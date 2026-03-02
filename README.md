# Workflow Automation

> 多端自动化工作流 - LangGraph 实现的前端代码生成系统

## 📖 项目概述

本项目是一个基于 LangGraph 框架的自动化工作流系统，用于实现从需求文档和设计稿到五端（iOS、Android、鸿蒙、H5、小程序）代码的自动生成、联调与提交。

### 核心功能

- 📄 **需求管理**: 基于 GitHub Issues 的需求追踪系统
- 🎨 **设计解析**: 通过 MasterGo Magic MCP 集成解析设计稿
- 🤖 **代码生成**: 基于大语言模型的多平台代码生成
- 🔄 **自动联调**: 基于 Mock 数据的前后端并行开发
- 📦 **代码提交**: 自动提交代码到各平台仓库
- 🧩 **组件管理**: 统一的跨平台组件库

## 🏗️ 仓库架构

```
workflow-automation/          # 工作流仓库（本仓库）
├── src/                      # 工作流源码
│   ├── graphs/              # LangGraph 工作流定义
│   ├── agents/              # 智能体代码
│   ├── tools/               # 工具集
│   ├── storage/             # 存储实现
│   └── utils/               # 工具函数
├── config/                   # 配置文件
├── docs/                     # 文档
│   ├── requirements/        # 需求文档
│   ├── design/              # 设计文档
│   ├── api/                 # API 文档
│   └── assets/              # 资源文件
├── scripts/                  # 脚本工具
├── repos.json               # 仓库配置
└── AGENTS.md                # 项目结构索引

5个独立平台仓库：
├── ios-login-app/           # iOS 代码
├── android-login-app/       # Android 代码
├── harmonyos-login-app/     # 鸿蒙代码
├── h5-login-app/            # H5 代码
└── miniprogram-login-app/   # 小程序代码
```

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+
- Git

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件：

```env
# GitHub 配置
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=xll-gif

# MasterGo 配置
MASTERGO_API_KEY=your_mastergo_api_key
MASTERGO_FILE_ID=your_file_id

# 大语言模型配置
LLM_API_KEY=your_llm_api_key
```

### 运行工作流

```bash
python -m src.main
```

详细说明请参考 [快速开始指南](docs/QUICK_START.md)

## 📚 文档

### 核心文档

- [快速开始指南](docs/QUICK_START.md) - 如何快速上手
- [AGENTS.md](AGENTS.md) - 项目结构索引
- [组件映射规则](repos.json) - 跨平台组件映射配置

### 集成指南

- [MasterGo 集成指南](docs/MASTERGO_INTEGRATION_GUIDE.md) - MasterGo 集成详细说明
- [Mock 服务指南](docs/MOCK_SERVICE_GUIDE.md) - Mock 数据服务使用指南

### 需求文档

- [需求文档模板](docs/requirements/REQUIREMENT_TEMPLATE.md) - 需求文档模板
- [登录页面需求](docs/requirements/REQ-001-login-page.md) - 登录页面需求示例

## 🛠️ 技术栈

### 工作流框架

- **LangGraph**: 工作流编排框架
- **LangChain**: LLM 应用框架
- **Python**: 核心开发语言

### 集成服务

- **GitHub Issues**: 需求管理
- **MasterGo**: 设计稿管理（Magic MCP）
- **GitHub API**: 代码仓库管理
- **Postman**: API 定义

### 平台技术栈

| 平台 | 语言 | 框架 | 架构 |
|-----|------|------|------|
| iOS | Swift 5.9+ | SwiftUI | MVVM |
| Android | Kotlin 1.9+ | Jetpack Compose | MVVM |
| 鸿蒙 | ArkTS | ArkUI | MVVM |
| H5 | TypeScript | React 18 + Vite | MVC |
| 小程序 | JavaScript | 微信原生 | MVP |

## 📦 已实现组件

| 组件 | iOS | Android | 鸿蒙 | H5 | 小程序 |
|-----|-----|---------|------|-----|--------|
| Button | ✅ | ✅ | ✅ | ✅ | ✅ |
| InputField | ✅ | ✅ | ✅ | ✅ | ✅ |
| Image | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Loading | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## 🔗 相关仓库

| 仓库名称 | 说明 | 链接 |
|---------|------|------|
| workflow-automation | 工作流仓库 | [GitHub](https://github.com/xll-gif/workflow-automation) |
| ios-login-app | iOS 应用 | [GitHub](https://github.com/xll-gif/ios-login-app) |
| android-login-app | Android 应用 | [GitHub](https://github.com/xll-gif/android-login-app) |
| harmonyos-login-app | 鸿蒙应用 | [GitHub](https://github.com/xll-gif/harmonyos-login-app) |
| h5-login-app | H5 应用 | [GitHub](https://github.com/xll-gif/h5-login-app) |
| miniprogram-login-app | 小程序应用 | [GitHub](https://github.com/xll-gif/miniprogram-login-app) |

## 📋 开发流程

### 1. 需求管理

使用 GitHub Issues 创建需求：

```bash
# 在 workflow-automation 仓库创建主 Issue
# 标题格式: [REQ-001] 登录页面
```

### 2. 设计稿准备

在 MasterGo 中创建设计稿，记录文件 ID。

### 3. 运行工作流

```bash
# 从需求文档生成代码
python -m src.main --requirement REQ-001
```

### 4. 代码审查

各平台仓库自动生成 Pull Request，进行代码审查。

### 5. 合并发布

审查通过后合并代码，触发自动构建和部署。

## 🤝 贡献指南

欢迎贡献代码、文档或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License

## 👥 联系方式

- GitHub: [@xll-gif](https://github.com/xll-gif)
- Issues: [GitHub Issues](https://github.com/xll-gif/workflow-automation/issues)

## 🗺️ 路线图

- [x] 仓库架构搭建
- [x] 基础组件开发（Button、InputField）
- [ ] 登录页面完整实现
- [ ] 商品卡片组件
- [ ] 订单列表组件
- [ ] 完整的 Mock 数据服务
- [ ] 自动化 CI/CD 流程
- [ ] 性能优化和测试覆盖

---

**Built with ❤️ using LangGraph**
