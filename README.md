# Workflow Automation - 工作流自动化系统

## 📖 项目简介

这是一个基于 LangGraph 的多端代码生成工作流系统，实现从需求文档和设计稿到五端（iOS、Android、鸿蒙、H5、小程序）代码的自动生成、联调与提交。

## 🏗️ 项目架构

```
workflow-automation/              # 工作流管理仓库（中心节点）
├── src/                          # 工作流源代码
│   ├── graphs/                   # 工作流编排
│   ├── agents/                   # 智能代理
│   ├── tools/                    # 工具函数
│   └── utils/                    # 工具类
├── config/                       # 配置文件
├── docs/                         # 文档
│   ├── requirements/             # 需求文档
│   ├── design/                   # 设计文档
│   └── setup/                    # 配置指南
├── assets/                       # 资源文件
├── scripts/                      # 脚本文件
│   ├── generate_tokens.py        # 设计令牌生成脚本
│   └── preview_workflow.py       # 工作流预览工具
├── config/                       # 配置文件
│   ├── design_tokens.json        # 设计令牌定义（跨平台样式规范）
│   └── tokens/                   # 各平台转换后的令牌文件（自动生成）
│       ├── ios_tokens.json
│       ├── android_tokens.json
│       ├── harmonyos_tokens.json
│       ├── h5_tokens.json
│       └── miniprogram_tokens.json
└── repos.json                    # 仓库配置

multi-platform-apps/              # 平台代码仓库（独立仓库）
├── ios-login-app/                # iOS 仓库
├── android-login-app/            # Android 仓库
├── harmonyos-login-app/          # 鸿蒙仓库
├── h5-login-app/                 # H5 仓库
└── miniprogram-login-app/        # 小程序仓库
```

## 🎨 设计令牌系统

本系统采用设计令牌（Design Tokens）实现跨平台样式一致性，确保五端视觉效果完全一致。

### 核心特性
- ✅ **单一数据源**：所有样式定义在 `config/design_tokens.json`
- ✅ **自动转换**：颜色、间距、单位等自动转换为各平台格式
- ✅ **易于维护**：修改一处，所有平台同步更新

### 快速使用

```bash
# 生成各平台令牌文件
python scripts/generate_tokens.py

# 查看令牌转换示例
cat config/tokens/ios_tokens.json
```

### 令牌转换示例

| 令牌 | iOS | Android | 鸿蒙 | H5 | 小程序 |
|------|-----|---------|------|-----|--------|
| `colors.primary.default` | `Color(hex: "#1890ff")` | `Color(0xFF1890FF)` | `"#1890ff"` | `#1890ff` | `#1890ff` |
| `spacing.md` | `16pt` | `16dp` | `16vp` | `16px` | `16rpx` |
| `components.button.height.md` | `40pt` | `40dp` | `40vp` | `40px` | `40rpx` |

详见：[设计令牌系统文档](./docs/DESIGN_TOKENS_SYSTEM.md)

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/xll-gif/workflow-automation.git
cd workflow-automation
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入必要的配置
# - GITHUB_TOKEN: GitHub Personal Access Token
# - MASTERGO_TOKEN: MasterGo API Token
# - LLM_API_KEY: 大语言模型 API Key
```

### 4. 预览工作流

在运行之前，您可以先预览工作流的结构：

```bash
# 使用预览工具查看工作流
python scripts/preview_workflow.py
```

这将显示：
- 📋 工作流节点列表（34 个节点）
- 🚀 工作流执行流程
- ⚡ 五端并行分支详情
- 📥📤 工作流输入输出
- 🎨 Mermaid 格式流程图（可在 Markdown 中渲染）

### 5. 配置 GitHub Token

详细配置步骤请参考：[GitHub Token 配置指南](docs/setup-github-token.md)

快速配置：
```bash
export GITHUB_TOKEN="your_github_token"
```

### 6. 运行工作流

```bash
# 方式 1: 启动 HTTP 服务
python src/main.py -m http -p 5000

# 方式 2: 直接运行流程
python src/main.py -m flow -i '{"repo_owner": "...", "mastergo_url": "..."}'

# 方式 3: 运行单个节点
python src/main.py -m node -n design_parse -i '{"mastergo_url": "..."}'
```

## 📋 需求管理

### 创建新需求

1. **创建需求文档**：
   ```bash
   cp docs/requirements/REQUIREMENT_TEMPLATE.md docs/requirements/REQ-XXX-feature-name.md
   ```

2. **编辑需求文档**：
   - 填写需求基本信息
   - 描述功能需求
   - 添加设计稿链接
   - 定义 API 接口
   - 明确验收标准

3. **创建 GitHub Issue**：
   - 访问 https://github.com/xll-gif/workflow-automation/issues
   - 点击 "New Issue"
   - 复制需求文档内容
   - 添加相关标签

### 现有需求

| 编号 | 名称 | 状态 | Issue | 优先级 |
|-----|------|------|-------|--------|
| REQ-001 | 登录页面 | 🚧 开发中 | [#1](https://github.com/xll-gif/workflow-automation/issues/1) | 🔴 高 |

## 🎨 设计稿管理

### MasterGo 集成

本系统使用 MasterGo 作为设计工具，通过官方 Magic MCP 服务器进行设计稿解析。

- **设计稿链接**: https://mastergo.com
- **集成方式**: @mastergo/magic-mcp

### 设计规范

设计规范文档位于 `docs/design/` 目录。

## 🤖 工作流程

### 完整流程图

```
需求文档 (GitHub Issue)
    ↓
设计稿 (MasterGo)
    ↓
组件识别 (LLM)
    ↓
五端并行代码生成
    ├─ iOS 代码
    ├─ Android 代码
    ├─ 鸿蒙代码
    ├─ H5 代码
    └─ 小程序代码
    ↓
代码收集
    ↓
代码审查 (LLM)
    ↓
自动化测试 (Mock)
    ↓
提交到 GitHub
    ↓
验收发布
```

### 工作流节点

1. **需求解析节点**
   - 读取 GitHub Issue
   - 解析需求文档
   - 提取功能清单

2. **设计稿解析节点**
   - 连接 MasterGo
   - 解析设计稿结构
   - 提取静态资源

3. **组件识别节点**
   - 识别设计组件
   - 匹配组件映射表
   - 确认组件类型

4. **五端并行代码生成节点**
   - iOS 代码生成（SwiftUI）
   - Android 代码生成（Jetpack Compose）
   - 鸿蒙代码生成（ArkUI）
   - H5 代码生成（React + TypeScript）
   - 小程序代码生成（原生小程序）

5. **代码审查节点**
   - 代码质量检查
   - 代码风格检查
   - 安全性检查

6. **自动化测试节点**
   - 单元测试
   - 集成测试
   - E2E 测试

7. **提交到 GitHub 节点**
   - 创建 Pull Request
   - 自动化 CI/CD
   - 代码合并

## 📊 工作流预览

### 使用预览工具

```bash
# 运行预览工具
python scripts/preview_workflow.py
```

这将显示：
- 工作流节点列表
- 执行流程
- 并行分支详情
- 输入输出参数
- Mermaid 流程图代码

### 在线可视化

访问 `/graph_parameter` 端点可以查看工作流的输入输出参数：

```bash
curl http://localhost:5000/graph_parameter
```

### Mermaid 流程图

预览工具会生成 Mermaid 格式的流程图代码，您可以：

1. 复制到 Markdown 文件中
2. 在 GitHub、GitLab 等平台会自动渲染
3. 或使用 [Mermaid Live Editor](https://mermaid.live/) 在线查看

## 🔧 配置文件

### 环境变量配置

```bash
# .env.example 示例

# GitHub 配置
GITHUB_TOKEN=your_github_token

# MasterGo 配置
MASTERGO_API_URL=https://api.mastergo.com
MASTERGO_MCP_TOKEN=your_mastergo_mcp_token

# 大模型配置
LLM_API_KEY=your_llm_api_key

# 对象存储配置（可选）
OSS_ACCESS_KEY_ID=your_oss_access_key
OSS_ACCESS_KEY_SECRET=your_oss_secret
OSS_BUCKET=your_bucket_name
OSS_ENDPOINT=your_oss_endpoint
```

### 仓库配置

`repos.json` 文件配置各平台的代码仓库：

```json
{
  "ios": {
    "repo": "xll-gif/ios-login-app",
    "branch": "main"
  },
  "android": {
    "repo": "xll-gif/android-login-app",
    "branch": "main"
  },
  "harmonyos": {
    "repo": "xll-gif/harmonyos-login-app",
    "branch": "main"
  },
  "h5": {
    "repo": "xll-gif/h5-login-app",
    "branch": "main"
  },
  "miniprogram": {
    "repo": "xll-gif/miniprogram-login-app",
    "branch": "main"
  }
}
```

## 📚 文档

- [AGENTS.md](AGENTS.md) - 项目结构索引，包含完整的节点清单
- [docs/](docs/) - 详细文档目录
- [README_API_SERVER.md](README_API_SERVER.md) - API 服务说明
- [TENCENT_COS_INTEGRATION_GUIDE.md](TENCENT_COS_INTEGRATION_GUIDE.md) - 腾讯云 COS 集成指南

## 🎯 支持的平台

| 平台 | 技术栈 | 代码风格 |
|------|--------|----------|
| iOS | SwiftUI | Swift |
| Android | Jetpack Compose | Kotlin |
| 鸿蒙 | ArkUI | ArkTS |
| H5 | React + TypeScript + Vite | TypeScript |
| 小程序 | 原生小程序 | JavaScript |

## 📈 版本历史

### v7.0（最新）
- ✨ 新增五端并行联调测试功能
- ✨ 新增自动修复功能
- 🐛 优化代码生成质量

### v6.0
- ✨ 新增代码拉取功能
- ✨ 新增项目规则分析功能
- ✨ 引入 Design Tokens 系统
- 🎨 跨平台样式一致性

### v5.0
- ✨ 新增 Git 推送功能
- 🎨 优化工作流编排

### v4.0
- ✨ 新增测试验证功能

### v3.0
- ✨ 新增五端代码生成功能

### v2.0
- ✨ 新增组件识别功能

### v1.0
- 🎉 初始版本
- 基础设计稿解析和资源处理

## 🛠️ 技术栈

- **工作流框架**: LangGraph
- **编程语言**: Python 3.9+
- **设计工具**: MasterGo（官方 Magic MCP）
- **对象存储**: 阿里云 OSS / 腾讯云 COS
- **模型能力**: 多模态大模型、代码生成大模型

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

- GitHub Issues: [https://github.com/xll-gif/workflow-automation/issues](https://github.com/xll-gif/workflow-automation/issues)
