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
└── repos.json                    # 仓库配置

multi-platform-apps/              # 平台代码仓库（独立仓库）
├── ios-login-app/                # iOS 仓库
├── android-login-app/            # Android 仓库
├── harmonyos-login-app/          # 鸿蒙仓库
├── h5-login-app/                 # H5 仓库
└── miniprogram-login-app/        # 小程序仓库
```

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

### 4. 配置 GitHub Token

详细配置步骤请参考：[GitHub Token 配置指南](docs/setup-github-token.md)

快速配置：
```bash
export GITHUB_TOKEN="your_github_token"
```

### 5. 运行工作流

```bash
python src/main.py
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
   - 生成 iOS 代码
   - 生成 Android 代码
   - 生成鸿蒙代码
   - 生成 H5 代码
   - 生成小程序代码

5. **代码收集节点**
   - 收集五端生成的代码
   - 整理代码结构

6. **代码审查节点 (v3.0 新增)**
   - 代码质量检查
   - 代码规范性验证
   - 潜在问题识别
   - 生成审查报告

7. **自动化测试节点 (v3.0 新增)**
   - 编写测试用例
   - 执行自动化测试
   - 生成测试报告

8. **代码提交节点**
   - 提交到各平台仓库
   - 创建 Pull Request
   - 更新 Issue 状态

## 🛠️ 技术栈

### 工作流框架
- **LangGraph**: 工作流编排
- **Python**: 主要编程语言
- **LangChain**: LLM 集成

### AI 能力
- **多模态大模型**: 设计稿识别
- **代码生成大模型**: 代码生成
- **NLP 模型**: 需求理解

### 工具集成
- **GitHub**: 代码仓库、Issues 管理
- **MasterGo**: 设计工具
- **Postman**: API 定义
- **OSS/S3**: 对象存储

### 前端技术栈
- **iOS**: SwiftUI
- **Android**: Jetpack Compose (Kotlin)
- **鸿蒙**: ArkTS
- **H5**: React 18 + TypeScript + Vite
- **小程序**: 原生小程序

## 📚 文档

- [需求文档模板](docs/requirements/REQUIREMENT_TEMPLATE.md)
- [GitHub Token 配置指南](docs/setup-github-token.md)
- [设计规范文档](docs/design/design-system.md)
- [API 文档](docs/api/authentication.md)
- [组件映射表](docs/component-mapping.md)

## 🔗 相关链接

### 代码仓库
- **Workflow**: [workflow-automation](https://github.com/xll-gif/workflow-automation)
- **iOS**: [ios-login-app](https://github.com/xll-gif/ios-login-app)
- **Android**: [android-login-app](https://github.com/xll-gif/android-login-app)
- **鸿蒙**: [harmonyos-login-app](https://github.com/xll-gif/harmonyos-login-app)
- **H5**: [h5-login-app](https://github.com/xll-gif/h5-login-app)
- **小程序**: [miniprogram-login-app](https://github.com/xll-gif/miniprogram-login-app)

### Issues
- [所有 Issues](https://github.com/xll-gif/workflow-automation/issues)
- [需求文档 Issues](https://github.com/xll-gif/workflow-automation/issues?q=label%3Arequirement)
- [Bug 报告](https://github.com/xll-gif/workflow-automation/issues?q=label%3Abug)

## 🤝 贡献指南

欢迎贡献代码、提出建议或报告问题！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 📞 联系方式

- **GitHub**: [@xll-gif](https://github.com/xll-gif)
- **Issues**: [提交问题](https://github.com/xll-gif/workflow-automation/issues)

---

**最后更新**: 2026-03-02
