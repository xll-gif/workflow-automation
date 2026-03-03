# 环境变量配置指南

本指南详细说明了工作流所需的所有环境变量配置。

## 概述

工作流支持多种配置，包括：
- GitHub 集成
- 对象存储（支持阿里云 OSS 和腾讯云 COS）
- 大语言模型
- MasterGo 设计稿解析

## 配置方式

### 方式 1：使用 `.env` 文件

创建 `.env` 文件：

```bash
cp .env.example .env
vim .env
```

### 方式 2：使用环境变量

在命令行中设置：

```bash
export GITHUB_TOKEN="your_token"
export LLM_API_KEY="your_api_key"
# ... 其他环境变量
```

### 方式 3：在运行时设置

```bash
GITHUB_TOKEN="your_token" LLM_API_KEY="your_api_key" python src/main.py
```

## 必需配置

### GitHub Token

**作用**：用于访问 GitHub 仓库，创建 Issue、推送代码

**获取方式**：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：`repo`（完整访问权限）
4. 生成并复制 Token

**环境变量**：
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 大语言模型 API Key

**作用**：用于代码生成、代码审查、测试用例生成

**支持模型**：
- OpenAI GPT-4
- OpenAI GPT-3.5
- 其他兼容 OpenAI API 的模型

**环境变量**：
```bash
export LLM_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export LLM_API_BASE="https://api.openai.com/v1"
export LLM_MODEL="gpt-4"
```

## 可选配置

### 对象存储配置

工作流支持多种对象存储后端：阿里云 OSS、腾讯云 COS、Mock 模式。

#### 阿里云 OSS（默认）

**作用**：用于存储静态资源（图片、图标等）

**获取方式**：
1. 访问阿里云 OSS 控制台
2. 创建 Bucket
3. 获取 AccessKey ID 和 Secret

**环境变量**：
```bash
export STORAGE_BACKEND="oss"
export OSS_ACCESS_KEY_ID="your_access_key_id"
export OSS_ACCESS_KEY_SECRET="your_access_key_secret"
export OSS_BUCKET="your_bucket_name"
export OSS_ENDPOINT="https://oss-cn-hangzhou.aliyuncs.com"
```

#### 腾讯云 COS

**作用**：用于存储静态资源（图片、图标等）

**获取方式**：
1. 访问腾讯云 COS 控制台
2. 创建存储桶
3. 配置后端 API（支持 STS 临时凭证）
4. 获取 API 配置信息

**环境变量**：
```bash
export STORAGE_BACKEND="cos"
export TENCENT_API_BASE_URL="https://your-backend-api.com"
export TENCENT_SCENE_NAME="frontend-automation"
export TENCENT_BUSINESS_NAME="workflow"
export TENCENT_MODE="dev"  # dev, test, prod
export TENCENT_TOKEN="your_token"
export TENCENT_SECRET_KEY="your_secret_key"
```

**参数说明**：
- `TENCENT_API_BASE_URL`：后端 API 地址，用于获取 STS 临时凭证
- `TENCENT_SCENE_NAME`：场景名称，用于区分不同业务场景
- `TENCENT_BUSINESS_NAME`：业务名称，用于标识业务方
- `TENCENT_MODE`：运行模式（dev/test/prod）
- `TENCENT_TOKEN`：认证 Token，用于后端 API 认证
- `TENCENT_SECRET_KEY`：密钥，用于签名验证

**STS 临时凭证机制**：
工作流通过后端 API 获取 STS 临时凭证，而不是直接使用永久密钥，更安全。

#### Mock 模式

用于开发和测试，不实际上传文件。

```bash
export STORAGE_BACKEND="mock"
```

### MasterGo 配置

**作用**：解析 MasterGo 设计稿，提取组件和资源

**环境变量**：
```bash
export MASTERGO_TOKEN="your_mastergo_token"
export USE_MOCK_MCP="false"  # true 表示使用 Mock 模式
```

**获取方式**：
1. 访问 MasterGo 官网
2. 登录并获取 API Token
3. 配置到环境变量

**Mock 模式**：
```bash
export USE_MOCK_MCP="true"
```

Mock 模式用于测试，不需要真实的 MasterGo Token。

## 完整配置示例

```bash
# GitHub Token（必需）
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 大语言模型（必需）
export LLM_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export LLM_API_BASE="https://api.openai.com/v1"
export LLM_MODEL="gpt-4"

# 对象存储（选择一种）
# 阿里云 OSS
export STORAGE_BACKEND="oss"
export OSS_ACCESS_KEY_ID="your_access_key_id"
export OSS_ACCESS_KEY_SECRET="your_access_key_secret"
export OSS_BUCKET="your_bucket_name"
export OSS_ENDPOINT="https://oss-cn-hangzhou.aliyuncs.com"

# 或 腾讯云 COS
# export STORAGE_BACKEND="cos"
# export TENCENT_API_BASE_URL="https://your-backend-api.com"
# export TENCENT_SCENE_NAME="frontend-automation"
# export TENCENT_BUSINESS_NAME="workflow"
# export TENCENT_MODE="dev"
# export TENCENT_TOKEN="your_token"
# export TENCENT_SECRET_KEY="your_secret_key"

# MasterGo（可选）
export MASTERGO_TOKEN="your_mastergo_token"
export USE_MOCK_MCP="false"
```

## 安全提示

1. **不要将 `.env` 文件提交到 Git 仓库**：`.env` 文件包含敏感信息，应该添加到 `.gitignore`
2. **使用最小权限原则**：GitHub Token 只给需要的权限
3. **定期轮换密钥**：定期更换 API Key 和 Token
4. **使用环境变量管理工具**：推荐使用 `direnv` 或 `python-dotenv` 管理环境变量

## 验证配置

运行以下命令验证配置：

```bash
python -c "
import os
from dotenv import load_dotenv

load_dotenv()

# 检查必需配置
if not os.getenv('GITHUB_TOKEN'):
    print('❌ GITHUB_TOKEN 未配置')
else:
    print('✅ GITHUB_TOKEN 已配置')

if not os.getenv('LLM_API_KEY'):
    print('❌ LLM_API_KEY 未配置')
else:
    print('✅ LLM_API_KEY 已配置')

# 检查对象存储配置
storage_backend = os.getenv('STORAGE_BACKEND', 'oss')
print(f'✅ 存储后端: {storage_backend.upper()}')

if storage_backend == 'oss':
    if all([os.getenv('OSS_ACCESS_KEY_ID'), os.getenv('OSS_ACCESS_KEY_SECRET'), os.getenv('OSS_BUCKET'), os.getenv('OSS_ENDPOINT')]):
        print('✅ 阿里云 OSS 配置完整')
    else:
        print('⚠️ 阿里云 OSS 配置不完整，将使用 Mock 模式')
elif storage_backend == 'cos':
    if os.getenv('TENCENT_API_BASE_URL'):
        print('✅ 腾讯云 COS 配置完整')
    else:
        print('⚠️ 腾讯云 COS 配置不完整，将使用 Mock 模式')
"
```

## 故障排查

### GitHub Token 无效

**问题**：`401 Unauthorized` 或 `Bad credentials`

**解决**：
1. 检查 Token 是否正确
2. 检查 Token 是否有 `repo` 权限
3. 检查 Token 是否已过期

### 对象存储上传失败

**问题**：无法上传文件到对象存储

**解决**：
1. 检查 AccessKey 是否正确
2. 检查 Bucket 是否存在
3. 检查 Endpoint 是否正确
4. 检查网络连接

### 腾讯云 COS 上传失败

**问题**：无法上传文件到腾讯云 COS

**解决**：
1. 检查 `TENCENT_API_BASE_URL` 是否正确
2. 检查后端 API 是否可访问
3. 检查 `TENCENT_TOKEN` 和 `TENCENT_SECRET_KEY` 是否正确
4. 检查后端 API 返回的 STS 凭证是否有效

### MasterGo Token 无效

**问题**：无法解析 MasterGo 设计稿

**解决**：
1. 检查 Token 是否正确
2. 检查 Token 是否已过期
3. 使用 Mock 模式测试：`export USE_MOCK_MCP="true"`

## 参考文档

- [GitHub Token 配置指南](setup-github-token.md)
- [MasterGo 集成指南](MASTERGO_INTEGRATION_GUIDE.md)
- [Mock 服务指南](MOCK_SERVICE_GUIDE.md)
- [代码审查与测试指南](CODE_REVIEW_AND_TEST_GUIDE.md)
