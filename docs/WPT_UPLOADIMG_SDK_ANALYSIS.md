# wpt-uploadImg SDK 接口分析

## SDK 概述

**仓库地址**: https://github.com/xll-gif/UploadXll/tree/main/wptresource/packages/uploadImg

**功能**: 图片上传 SDK，兼容 H5 和小程序，支持腾讯云 COS 上传

## 核心配置参数

### 必需参数

| 参数名 | 类型 | 说明 | 示例值 |
|-------|------|------|--------|
| `sceneName` | string | 应用场景名称，需要去资源中心申请 | `'wechatCx'`、`'imchat'` |
| `businessName` | string | 业务名称英文名，需要去资源中心申请 | `'kefu'`、`'sale'` |
| `mode` | string | 运行环境 | `'dev'`、`'gray'`、`'prod'` |
| `token` | string | 认证 Token | `'your-token'` |

### 可选参数

| 参数名 | 类型 | 说明 | 示例值 |
|-------|------|------|--------|
| `env` | string | 运行环境（仅 H5） | `'h5'`、`'wechat'` |
| `limit` | number | 单次上传数量限制 | `9` |
| `maxSize` | number | 大小限制（字节） | `10 * 1024 * 1024` |
| `onProgress` | function | 上传进度回调 | `(percent, index) => {}` |
| `secretKey` | string | X-Secret-Key 值，优先从 cookie 获取 | `'your-secret-key'` |

## 上传流程

### 1. 获取上传凭证

SDK 内部会调用后端接口获取腾讯云 COS 的 STS 临时凭证：

**接口**: `/api/v1/upload-token`

**请求方式**: GET

**请求头**:
```
Authorization: Bearer {token}
X-Secret-Key: {secretKey}  // 可选，优先从 cookie 获取
```

**请求参数**:
```
sceneName={sceneName}
businessName={businessName}
mode={mode}
```

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "credentials": {
      "tmpSecretId": "xxx",
      "tmpSecretKey": "xxx",
      "sessionToken": "xxx",
      "expiredTime": 1800
    },
    "bucket": "your-bucket",
    "region": "ap-guangzhou",
    "cosdomain": "cos.ap-guangzhou.myqcloud.com"
  }
}
```

### 2. 上传文件

使用获取到的 STS 凭证，初始化腾讯云 COS SDK 并上传文件。

### 3. 上报结果

上传成功后，SDK 会调用后端接口上报上传结果。

## 后端 API 配置

根据 `mode` 参数，SDK 会请求不同环境的资源中心：

| mode | API 域名 | 说明 |
|------|---------|------|
| `dev` | https://skt.weipaitang.com | 开发环境 |
| `gray` | https://canary-sk.weipaitang.com | 灰度环境 |
| `prod` | https://sk.weipaitang.com | 生产环境 |

## 小程序合法域名配置

### request 合法域名

1. https://skt.weipaitang.com
2. https://canary-sk.weipaitang.com
3. https://sk.weipaitang.com

### uploadFile 合法域名

需要根据具体环境的 bucket 添加合法域名。

## 使用示例

### H5 环境示例

```javascript
import UploadImg from "wpt-uploadImg";

const uploadImg = new UploadImg({
  sceneName: 'wechatCx',
  businessName: 'kefu',
  mode: 'dev',
  env: 'h5',
  token: 'your-token',
  limit: 9,
  maxSize: 10 * 1024 * 1024,
  onProgress: (percent, index) => {
    console.log(`上传进度: ${percent}%, 图片索引: ${index}`);
  },
  secretKey: 'your-secret-key'  // 可选
});

// 上传文件（让用户选择）
uploadImg.upload().then(
  (res) => {
    console.log("上传成功:", res);
    // res 格式:
    // [
    //   { url: 'https://bucket.cos.region.myqcloud.com/xxx.png', key: 'xxx.png' },
    //   ...
    // ]
  },
  (err) => {
    console.log("上传失败:", err);
  }
);

// 上传文件（传入文件数组）
uploadImg.upload([file1, file2]).then(
  (res) => {
    console.log("上传成功:", res);
  },
  (err) => {
    console.log("上传失败:", err);
  }
);
```

### 小程序环境示例

```javascript
import UploadImg from "wpt-uploadImg/dist/XcxUploadImg";

const uploadImg = new UploadImg({
  sceneName: 'wechatCx',
  businessName: 'kefu',
  mode: 'dev',
  token: 'your-token',
  limit: 9,
  maxSize: 10 * 1024 * 1024,
  onProgress: (percent, index) => {
    console.log(`上传进度: ${percent}%, 图片索引: ${index}`);
  },
  secretKey: 'your-secret-key'  // 可选
});

// 上传文件（调起 wx.chooseImage）
uploadImg.upload().then(
  (res) => {
    console.log("上传成功:", res);
  },
  (err) => {
    console.log("上传失败:", err);
  }
);

// 上传文件（传入文件数组）
uploadImg.upload(wx.chooseImage({ count: 1 }).tempFiles).then(
  (res) => {
    console.log("上传成功:", res);
  },
  (err) => {
    console.log("上传失败:", err);
  }
);
```

## Python 后端实现方案

### 1. 获取上传凭证接口

```python
import requests
from typing import Dict, Any, Optional

def get_upload_token(
    scene_name: str,
    business_name: str,
    mode: str,
    token: str,
    secret_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取腾讯云 COS 上传凭证

    Args:
        scene_name: 应用场景名称
        business_name: 业务名称
        mode: 运行环境（dev/gray/prod）
        token: 认证 Token
        secret_key: X-Secret-Key 值（可选）

    Returns:
        上传凭证信息
    """
    # 根据模式选择 API 域名
    api_domains = {
        'dev': 'https://skt.weipaitang.com',
        'gray': 'https://canary-sk.weipaitang.com',
        'prod': 'https://sk.weipaitang.com'
    }

    api_base_url = api_domains.get(mode, 'https://skt.weipaitang.com')

    # 构建请求 URL
    url = f"{api_base_url}/api/v1/upload-token"
    params = {
        'sceneName': scene_name,
        'businessName': business_name,
        'mode': mode
    }

    # 构建请求头
    headers = {
        'Authorization': f'Bearer {token}'
    }

    if secret_key:
        headers['X-Secret-Key'] = secret_key

    # 发送请求
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    if data.get('code') != 200:
        raise Exception(f"获取上传凭证失败: {data.get('message', '未知错误')}")

    return data.get('data', {})
```

### 2. 上传文件到 COS

```python
import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from typing import Optional, Callable

def upload_to_cos(
    file_path: str,
    credentials: Dict[str, Any],
    bucket: str,
    region: str,
    object_key: str,
    on_progress: Optional[Callable[[int, int], None]] = None
) -> str:
    """
    上传文件到腾讯云 COS

    Args:
        file_path: 本地文件路径
        credentials: STS 凭证信息
        bucket: 存储桶名称
        region: 地域
        object_key: 对象键
        on_progress: 上传进度回调

    Returns:
        文件 URL
    """
    # 配置 COS 客户端
    config = CosConfig(
        Region=region,
        SecretId=credentials['tmpSecretId'],
        SecretKey=credentials['tmpSecretKey'],
        Token=credentials['sessionToken'],
        Scheme='https'
    )

    client = CosS3Client(config)

    # 上传文件
    with open(file_path, 'rb') as fp:
        response = client.put_object(
            Bucket=bucket,
            Body=fp,
            Key=object_key,
            EnableMD5=False
        )

    # 返回文件 URL
    file_url = f"https://{bucket}.cos.{region}.myqcloud.com/{object_key}"

    return file_url
```

### 3. 完整上传流程

```python
import os
import uuid
from typing import List, Dict, Any

def upload_file_to_wpt_cos(
    file_path: str,
    scene_name: str,
    business_name: str,
    mode: str,
    token: str,
    secret_key: Optional[str] = None,
    prefix: str = "assets/"
) -> Dict[str, Any]:
    """
    上传文件到 WPT 腾讯云 COS

    Args:
        file_path: 本地文件路径
        scene_name: 应用场景名称
        business_name: 业务名称
        mode: 运行环境（dev/gray/prod）
        token: 认证 Token
        secret_key: X-Secret-Key 值（可选）
        prefix: 上传前缀

    Returns:
        上传结果
    """
    # 1. 获取上传凭证
    credentials_info = get_upload_token(
        scene_name=scene_name,
        business_name=business_name,
        mode=mode,
        token=token,
        secret_key=secret_key
    )

    credentials = credentials_info['credentials']
    bucket = credentials_info['bucket']
    region = credentials_info['region']

    # 2. 生成对象键
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1]
    object_key = f"{prefix}{uuid.uuid4()}{ext}"

    # 3. 上传文件
    file_url = upload_to_cos(
        file_path=file_path,
        credentials=credentials,
        bucket=bucket,
        region=region,
        object_key=object_key
    )

    return {
        'url': file_url,
        'key': object_key,
        'bucket': bucket,
        'region': region
    }
```

## 工作流集成配置

### 环境变量配置

```bash
# WPT 资源中心配置
WPT_SCENE_NAME=wechatCx  # 应用场景名称
WPT_BUSINESS_NAME=kefu  # 业务名称
WPT_MODE=dev  # 运行环境（dev/gray/prod）
WPT_TOKEN=your-token  # 认证 Token
WPT_SECRET_KEY=your-secret-key  # X-Secret-Key（可选）

# 根据模式自动选择 API 域名
# dev: https://skt.weipaitang.com
# gray: https://canary-sk.weipaitang.com
# prod: https://sk.weipaitang.com
```

### API 域名映射

```python
WPT_API_DOMAINS = {
    'dev': 'https://skt.weipaitang.com',
    'gray': 'https://canary-sk.weipaitang.com',
    'prod': 'https://sk.weipaitang.com'
}
```

## 注意事项

1. **sceneName 和 businessName 需要申请**: 需要去资源中心（余尧/李大双）申请
2. **secretKey 优先从 cookie 获取**: 如果 cookie 中没有，再从参数获取
3. **小程序需要配置合法域名**: 需要在微信小程序后台配置 request 和 uploadFile 合法域名
4. **STS 凭证有过期时间**: 需要在凭证过期前重新获取
5. **文件大小限制**: 需要根据业务需求配置 maxSize

## 参考资料

- **SDK 仓库**: https://github.com/xll-gif/UploadXll/tree/main/wptresource/packages/uploadImg
- **腾讯云 COS SDK**: https://cloud.tencent.com/document/product/436
- **STS 临时凭证**: https://cloud.tencent.com/document/product/436/14118
