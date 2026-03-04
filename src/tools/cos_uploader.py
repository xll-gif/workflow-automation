"""
腾讯云 COS 上传工具（WPT 资源中心版本）

使用 WPT 资源中心的接口获取 STS 临时凭证，然后上传到腾讯云 COS
"""
import os
import time
import uuid
import logging
import requests
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass

# 导入 qcloud_cos SDK（如果不存在则跳过，运行时会处理）
try:
    from qcloud_cos import CosConfig
    from qcloud_cos import CosS3Client
    QCLOUD_COS_AVAILABLE = True
except ImportError:
    QCLOUD_COS_AVAILABLE = False
    CosConfig = None
    CosS3Client = None

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WPT 资源中心 API 域名映射
WPT_API_DOMAINS = {
    'dev': 'https://skt.weipaitang.com',
    'gray': 'https://canary-sk.weipaitang.com',
    'prod': 'https://sk.weipaitang.com'
}


@dataclass
class STSCredentials:
    """STS 临时凭证"""
    tmp_secret_id: str
    tmp_secret_key: str
    session_token: str
    expired_time: int  # 过期时间（秒）
    bucket: str
    region: str
    cosdomain: Optional[str] = None


@dataclass
class UploadResult:
    """上传结果"""
    success: bool = False
    url: str = ""
    filename: str = ""
    key: str = ""
    bucket: str = ""
    region: str = ""
    size: int = 0
    error: Optional[str] = None


class WPTCOSUploader:
    """WPT 腾讯云 COS 上传器"""

    def __init__(
        self,
        scene_name: str = "wechatCx",
        business_name: str = "kefu",
        mode: str = "dev",
        token: Optional[str] = None,
        secret_key: Optional[str] = None
    ):
        """
        初始化 WPT 腾讯云 COS 上传器

        Args:
            scene_name: 应用场景名称（如 imchat, wechatCx）
            business_name: 业务名称英文名（如 sale, kefu）
            mode: 运行环境（dev/gray/prod）
            token: 认证 Token
            secret_key: X-Secret-Key 值（可选）
        """
        self.scene_name = scene_name
        self.business_name = business_name
        self.mode = mode
        self.token = token or os.getenv("WPT_TOKEN")
        self.secret_key = secret_key or os.getenv("WPT_SECRET_KEY")

        # 根据模式获取 API 域名
        self.api_base_url = WPT_API_DOMAINS.get(mode, WPT_API_DOMAINS['dev'])

        # STS 凭证缓存
        self.sts_credentials: Optional[STSCredentials] = None
        self.credentials_expires_at: float = 0

        # COS 客户端
        self.cos_client = None

        logger.info(f"WPT COS 上传器初始化成功")
        logger.info(f"  API 域名: {self.api_base_url}")
        logger.info(f"  场景名称: {self.scene_name}")
        logger.info(f"  业务名称: {self.business_name}")
        logger.info(f"  运行环境: {self.mode}")

    def get_upload_token(self) -> STSCredentials:
        """
        获取上传凭证（STS 临时凭证）

        调用 WPT 资源中心接口获取腾讯云 COS 的 STS 临时凭证

        Returns:
            STSCredentials 对象

        Raises:
            Exception: 获取凭证失败
        """
        # 检查缓存是否有效
        if (self.sts_credentials and
            self.credentials_expires_at and
            time.time() < self.credentials_expires_at):
            logger.info("使用缓存的 STS 凭证")
            return self.sts_credentials

        logger.info("从 WPT 资源中心获取新的 STS 凭证")

        # 构建请求 URL
        url = f"{self.api_base_url}/api/v1/upload-token"
        params = {
            'sceneName': self.scene_name,
            'businessName': self.business_name,
            'mode': self.mode
        }

        # 构建请求头
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        # 添加 X-Secret-Key（如果存在）
        if self.secret_key:
            headers['X-Secret-Key'] = self.secret_key

        try:
            # 发送请求
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()

            # 检查响应状态
            if data.get('code') != 200:
                error_msg = data.get('message', '未知错误')
                raise Exception(f"获取上传凭证失败: {error_msg}")

            # 解析凭证信息
            credentials_data = data.get('data', {})
            credentials_info = credentials_data.get('credentials', {})

            # 创建 STSCredentials 对象
            self.sts_credentials = STSCredentials(
                tmp_secret_id=credentials_info.get('tmpSecretId', ''),
                tmp_secret_key=credentials_info.get('tmpSecretKey', ''),
                session_token=credentials_info.get('sessionToken', ''),
                expired_time=credentials_info.get('expiredTime', 1800),
                bucket=credentials_data.get('bucket', ''),
                region=credentials_data.get('region', ''),
                cosdomain=credentials_data.get('cosdomain', '')
            )

            # 设置过期时间（提前 5 分钟过期）
            self.credentials_expires_at = time.time() + self.sts_credentials.expired_time - 300

            logger.info(f"STS 凭证获取成功，bucket: {self.sts_credentials.bucket}, region: {self.sts_credentials.region}")

            return self.sts_credentials

        except requests.exceptions.RequestException as e:
            logger.error(f"获取上传凭证失败（网络错误）: {e}")
            raise Exception(f"网络请求失败: {e}")
        except Exception as e:
            logger.error(f"获取上传凭证失败: {e}")
            raise

    def initialize_cos_client(self, credentials: STSCredentials):
        """
        初始化腾讯云 COS 客户端

        Args:
            credentials: STS 凭证
        """
        if not QCLOUD_COS_AVAILABLE:
            logger.error("未安装 qcloud_cos 包，正在安装...")
            os.system("pip install cos-python-sdk-v5")
            # 重新导入
            from qcloud_cos import CosConfig as ReloadedCosConfig
            from qcloud_cos import CosS3Client as ReloadedCosS3Client
            cos_config_class = ReloadedCosConfig
            cos_client_class = ReloadedCosS3Client
        else:
            cos_config_class = CosConfig
            cos_client_class = CosS3Client
        
        try:
            # 配置 COS 客户端
            config = cos_config_class(
                Region=credentials.region,
                SecretId=credentials.tmp_secret_id,
                SecretKey=credentials.tmp_secret_key,
                Token=credentials.session_token,
                Scheme='https'
            )

            self.cos_client = cos_client_class(config)

            logger.info("COS 客户端初始化成功")

        except Exception as e:
            logger.error(f"COS 客户端初始化失败: {e}")
            raise

    def upload_file(
        self,
        file_path: str,
        filename: Optional[str] = None,
        prefix: str = "assets/",
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> UploadResult:
        """
        上传文件到腾讯云 COS

        Args:
            file_path: 本地文件路径
            filename: 文件名（可选，默认使用原文件名）
            prefix: 上传前缀
            on_progress: 上传进度回调

        Returns:
            UploadResult 对象
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise Exception(f"文件不存在: {file_path}")

            # 获取文件信息
            file_size = os.path.getsize(file_path)
            original_filename = os.path.basename(file_path)
            upload_filename = filename or original_filename

            # 获取 STS 凭证
            credentials = self.get_upload_token()

            # 初始化 COS 客户端（如果还没初始化）
            if not self.cos_client:
                self.initialize_cos_client(credentials)

            # 生成对象键
            ext = os.path.splitext(upload_filename)[1]
            object_key = f"{prefix}{uuid.uuid4()}{ext}"

            logger.info(f"开始上传文件: {upload_filename} -> {object_key}")
            logger.info(f"  Bucket: {credentials.bucket}")
            logger.info(f"  Region: {credentials.region}")
            logger.info(f"  文件大小: {file_size} bytes")

            # 上传文件
            with open(file_path, 'rb') as fp:
                response = self.cos_client.put_object(
                    Bucket=credentials.bucket,
                    Body=fp,
                    Key=object_key,
                    EnableMD5=False
                )

            # 生成文件 URL
            file_url = f"https://{credentials.bucket}.cos.{credentials.region}.myqcloud.com/{object_key}"

            logger.info(f"文件上传成功: {file_url}")

            # 调用进度回调
            if on_progress:
                on_progress(100, 0)

            return UploadResult(
                success=True,
                url=file_url,
                filename=upload_filename,
                key=object_key,
                bucket=credentials.bucket,
                region=credentials.region,
                size=file_size
            )

        except Exception as e:
            logger.error(f"文件上传失败: {e}")
            return UploadResult(
                success=False,
                error=str(e)
            )

    def upload_and_report(
        self,
        file_path: str,
        filename: Optional[str] = None,
        prefix: str = "assets/",
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> UploadResult:
        """
        上传文件并上报结果

        Args:
            file_path: 本地文件路径
            filename: 文件名
            prefix: 上传前缀
            on_progress: 上传进度回调

        Returns:
            UploadResult 对象
        """
        # 上传文件
        result = self.upload_file(file_path, filename, prefix, on_progress)

        # 如果上传成功，上报结果到 WPT 资源中心
        if result.success:
            try:
                self.report_upload_result(result)
            except Exception as e:
                logger.warning(f"上报上传结果失败: {e}")

        return result

    def report_upload_result(self, result: UploadResult):
        """
        上报上传结果到 WPT 资源中心

        Args:
            result: 上传结果
        """
        logger.info("上报上传结果到 WPT 资源中心")

        # TODO: 实现上报逻辑
        # 需要确认 WPT 资源中心的上报接口

        logger.info("上报成功")


# 向后兼容：TencentCOSUploader 类
class TencentCOSUploader(WPTCOSUploader):
    """
    腾讯云 COS 上传器（向后兼容的别名）

    该类已被 WPTCOSUploader 替代，保留此别名以保持向后兼容
    """

    def __init__(
        self,
        api_base_url: Optional[str] = None,  # 已弃用，自动根据 mode 选择
        scene_name: str = "wechatCx",
        business_name: str = "kefu",
        mode: str = "dev",
        token: Optional[str] = None,
        secret_key: Optional[str] = None
    ):
        """
        初始化腾讯云 COS 上传器（向后兼容）

        Args:
            api_base_url: 已弃用，自动根据 mode 选择
            scene_name: 场景名称
            business_name: 业务名称
            mode: 环境模式
            token: 认证 Token
            secret_key: X-Secret-Key
        """
        if api_base_url:
            logger.warning("api_base_url 参数已弃用，将根据 mode 自动选择 API 域名")

        super().__init__(
            scene_name=scene_name,
            business_name=business_name,
            mode=mode,
            token=token,
            secret_key=secret_key
        )
