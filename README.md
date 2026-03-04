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
│   └── generate_tokens.py        # 设计令牌生成脚本
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

8. **Git 推送节点 (v5.0 新增)**
   - 推送 H5 代码到 GitHub
   - 推送 iOS 代码到 GitHub
   - 推送 Android 代码到 GitHub
   - 推送鸿蒙代码到 GitHub
   - 推送小程序代码到 GitHub

9. **代码提交节点**
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

## 📊 推送状态

### 登录页面五端代码推送结果

#### 初始推送

| 平台 | 仓库 | 提交哈希 | 状态 |
|------|------|---------|------|
| H5 | xll-gif/h5-login-app | 3704f9cf75ee8eabf6e8cc008994b677dd24d5f1 | ✅ 成功 |
| iOS | xll-gif/ios-login-app | 32fda2faf8e9c0b8b4d5239d34ded1de35b00c9f | ✅ 成功 |
| Android | xll-gif/android-login-app | fd27b032f68f2ed1559e8c68b636a2cdb14e983b | ✅ 成功 |
| 鸿蒙 | xll-gif/harmonyos-login-app | 6a23037a5ae96ead1cdb1b0707f2c3f6e91b1718 | ✅ 成功 |
| 小程序 | xll-gif/miniprogram-login-app | 7fa5c292c241f5733d363e3a5d5d0a3dae99478c | ✅ 成功 |

**推送时间**: 2025-06-20  
**推送方式**: 自动化工作流 + GitPusher 工具  
**提交信息**: `feat: #2 登录页面完整开发 - 用户名输入框, 密码输入框, 登录按钮`

#### 样式修复推送

| 平台 | 仓库 | 提交哈希 | 状态 |
|------|------|---------|------|
| H5 | xll-gif/h5-login-app | 264830450b8f7385e9e9f3e3eb530e387e56a68f | ✅ 成功 |
| iOS | xll-gif/ios-login-app | 27a14541b92afd64ecb97f70f0b88e4870d70bbc | ✅ 成功 |
| Android | xll-gif/android-login-app | 38fd7d0f5e648301ed45b8604ff0d8530e5303e | ✅ 成功 |
| 鸿蒙 | xll-gif/harmonyos-login-app | 884df0fe8ae2a0bf2cde9d5270eb9c8719782a10 | ✅ 成功 |
| 小程序 | xll-gif/miniprogram-login-app | 97e7dfe03b3c7f84a16c738f658762b707c86246 | ✅ 成功 |

**修复时间**: 2025-06-20  
**修复方式**: 批量修复脚本 + GitPusher 工具  
**提交信息**: `fix: 修复样式问题 - 优化布局、颜色转换、单位使用等`

#### 间距和居中修复推送

| 平台 | 仓库 | 提交哈希 | 状态 |
|------|------|---------|------|
| H5 | xll-gif/h5-login-app | 87f88616405f6838a0f77a5eb4a04c6f67e42d39 | ✅ 成功 |
| iOS | xll-gif/ios-login-app | 3c82d38b8984a6e0c7b7d969ca143cc7b729b8b7 | ✅ 成功 |
| Android | xll-gif/android-login-app | 7a8d58c82c2abea3c51c8063163c2865c36e8fc4 | ✅ 成功 |
| 鸿蒙 | xll-gif/harmonyos-login-app | 389fc57d890bcaa5e5684b63e04bd3ba93c0250d | ✅ 成功 |
| 小程序 | xll-gif/miniprogram-login-app | 3823ca53241fd6cd38e78d44c7ec0658e2248839 | ✅ 成功 |

**修复时间**: 2025-06-20  
**修复方式**: 批量修复脚本 + GitPusher 工具  
**提交信息**: `fix: 修复间距和居中问题 - 确保内容垂直水平居中`

## 📚 文档

- [推送成功报告](docs/PUSH_SUCCESS_REPORT.md) - 五端代码推送详情
- [样式修复报告](docs/STYLE_FIX_REPORT.md) - 样式问题修复详情
- [间距和居中修复报告](docs/SPACING_CENTER_FIX_REPORT.md) - 间距和居中修复详情
- [项目结构修复报告](docs/PROJECT_STRUCTURE_FIX_REPORT.md) - iOS 和 Android 项目结构修复详情
- [快速开始指南](docs/QUICK_START.md) - 各平台快速开始指南

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

**最后更新**: 2026-03-03

## 📝 更新日志

### 2026-03-03
- ✅ 实现设计令牌（Design Tokens）系统
- ✅ 统一五端颜色、间距、字体等样式规范
- ✅ 自动转换为各平台特定格式（颜色、单位等）
- ✅ 创建设计令牌转换工具类
- ✅ 生成各平台令牌文件
- ✅ 修复 iOS 项目结构，清理重复文件
- ✅ 删除根目录重复的 Swift 文件
- ✅ 删除重复的 Xcode 项目文件
- ✅ 确保项目符合 Xcode 标准结构

