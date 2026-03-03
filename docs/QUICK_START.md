# 工作流快速开始指南

## 概述

本指南帮助你快速开始使用企业前端工程师自动化工作流。

## 前置条件

1. ✅ GitHub 仓库已创建（workflow-automation + 5个平台仓库）
2. ✅ GitHub Token 已配置（需要 repo 权限）
3. ✅ MasterGo Token 已配置（如需使用设计稿解析功能）
4. ✅ 对象存储已配置（用于静态资源管理）

## 快速开始

### 步骤 1：配置环境变量

复制环境变量模板并编辑：

```bash
cp .env.example .env
vim .env
```

填入必要的配置：
- `GITHUB_TOKEN`: GitHub Personal Access Token（需要 repo 权限）
- `MASTERGO_TOKEN`: MasterGo API Token
- `LLM_API_KEY`: 大语言模型 API Key
- `OSS_ACCESS_KEY_ID`: 对象存储 Access Key
- `OSS_ACCESS_KEY_SECRET`: 对象存储 Secret Key

**GitHub Token 配置指南：**
```bash
export GITHUB_TOKEN="your_github_token"
```

详细配置步骤请参考：[GitHub Token 配置指南](setup-github-token.md)

### 步骤 2：创建 MasterGo 设计稿（可选）

如果你有设计稿，工作流可以解析设计稿并生成更准确的代码。

#### 2.1 访问 MasterGo

1. 访问 https://mastergo.com 并登录
2. 创建新文件
3. 设计你的页面（登录页、商品卡片等）

#### 2.2 获取设计稿链接

在 MasterGo 中打开设计稿，复制 URL 链接。

### 步骤 3：创建一个需求 Issue

#### 方式 A：使用需求模板

1. 复制需求模板：
   ```bash
   cp docs/requirements/REQUIREMENT_TEMPLATE.md docs/requirements/REQ-XXX-feature-name.md
   ```

2. 编辑需求文档：
   ```bash
   vim docs/requirements/REQ-XXX-feature-name.md
   ```

3. 填写需求信息：
   - 需求描述
   - 功能列表
   - MasterGo 设计稿链接
   - API 定义
   - 验收标准

4. 创建 GitHub Issue：
   - 访问 https://github.com/xll-gif/workflow-automation/issues
   - 点击 "New Issue"
   - 复制需求文档内容
   - 添加相关标签（如：`login-page`、`high-priority`）

**需求格式示例：**

```markdown
## 需求描述

开发一个用户登录功能，支持邮箱和密码登录，包含表单验证和错误提示。

## 功能列表

1. 实现登录页面 UI（使用 MasterGo 设计稿）
2. 实现邮箱输入框和验证
3. 实现密码输入框和验证
4. 实现登录按钮和点击事件
5. 实现表单验证功能
6. 实现错误提示显示
7. 实现登录接口调用
8. 实现登录成功跳转

## MasterGo 设计稿
MasterGo URL: https://mastergo.com/workspace/your-design-link

## API 定义

API: POST /api/auth/login
说明: 用户登录接口
请求参数：
{
  "email": "string",
  "password": "string"
}
响应参数：
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "string",
    "user": {
      "id": "string",
      "name": "string"
    }
  }
}

## 验收标准

1. 登录页面 UI 与设计稿一致
2. 邮箱和密码格式验证正确
3. 登录成功后跳转到首页
4. 错误提示清晰可见
5. 代码符合规范，通过代码审查
6. 测试用例覆盖率 ≥ 80%
```

### 步骤 4：运行工作流

```bash
python src/main.py
```

按照提示输入：
1. GitHub Issue URL
2. MasterGo 设计稿 URL（可选）

### 步骤 5：查看工作流输出

工作流会自动执行以下步骤：

```
开始
  ↓
1. 需求分析（从 GitHub Issues 获取需求）
  ↓
2. 设计稿解析（解析 MasterGo 设计稿）
  ↓
3. 静态资源上传（上传到对象存储）
  ↓
4. 组件识别（使用 AI 识别设计组件）
  ↓
5. 五端并行代码生成 ⚡
  ├─ iOS 代码（SwiftUI）
  ├─ Android 代码（Jetpack Compose）
  ├─ 鸿蒙代码（ArkTS）
  ├─ H5 代码（React + TypeScript）
  └─ 小程序代码（WXML + WXSS）
  ↓
6. 代码收集（汇总所有平台代码）
  ↓
7. [代码审查 + 自动化测试] ⚡ 并行执行
  ├─ 代码审查（质量、规范、安全检查）
  └─ 自动化测试（单元测试、集成测试）
  ↓
8. 推送到 GitHub（提交到各平台仓库）
  ↓
结束
```

## 工作流输出

工作流完成后，你会得到：

1. **五端代码**：
   - H5 代码：`repos/h5-login-app/`
   - iOS 代码：`repos/ios-login-app/`
   - Android 代码：`repos/android-login-app/`
   - 鸿蒙代码：`repos/harmonyos-login-app/`
   - 小程序代码：`repos/miniprogram-login-app/`

2. **代码审查报告**：`assets/code_review_report.json`
   - 代码质量评分（0-10）
   - 问题列表（critical/high/medium/low）
   - 改进建议

3. **测试报告**：`assets/test_report.json`
   - 测试用例列表
   - 测试结果
   - 测试覆盖率

4. **GitHub 提交**：
   - 各平台代码仓库的提交 URL
   - Pull Request（如需）

## 现有需求

| 编号 | 名称 | 状态 | Issue | 优先级 |
|-----|------|------|-------|--------|
| REQ-001 | 登录页面 | 🚧 开发中 | [#1](https://github.com/xll-gif/workflow-automation/issues/1) | 🔴 高 |

## MasterGo 集成说明

工作流通过官方 Magic MCP 服务器集成 MasterGo：
- **集成方式**：`@mastergo/magic-mcp`
- **功能**：解析设计稿结构、提取组件列表、提取静态资源
- **配置**：`config/mastergo_config.json`

详细指南请参考：[MasterGo 集成指南](MASTERGO_INTEGRATION_GUIDE.md)

## 代码审查说明（v3.0 新增）

代码审查节点会自动检查以下内容：
- 代码规范（命名、格式、注释）
- 代码质量（逻辑、边界处理、错误处理）
- 安全性（SQL注入、XSS、权限验证）
- 性能（算法复杂度、资源使用）
- 可维护性（模块化、可读性、可扩展性）

## 自动化测试说明（v3.0 新增）

自动化测试节点会：
- 为生成的代码编写测试用例
- 执行单元测试、集成测试、端到端测试
- H5 平台可实际运行 Vitest 测试
- 生成测试报告和覆盖率统计

## 常见问题

### Q: 如何配置 GitHub Token？

A: 参考 [GitHub Token 配置指南](setup-github-token.md)。确保 Token 具有 `repo` 权限。

### Q: 工作流支持哪些平台？

A: 目前支持以下平台：
- iOS（SwiftUI）
- Android（Jetpack Compose + Kotlin）
- 鸿蒙（ArkTS + ArkUI）
- H5（React 18 + TypeScript + Vite）
- 小程序（WXML + WXSS + JS）

### Q: 代码审查和测试会自动执行吗？

A: 是的。v3.0 版本中，代码审查和自动化测试会自动执行，并且并行运行以提升效率。

### Q: 如何查看代码审查报告？

A: 工作流完成后，审查报告会保存在 `assets/code_review_report.json`，包含详细的评分和改进建议。

### Q: H5 代码如何运行？

A: H5 代码使用 Vite 构建，进入项目目录后：
```bash
cd repos/h5-login-app
npm install
npm run dev
```

## 下一步

- 查看详细文档：
  - [MasterGo 集成指南](MASTERGO_INTEGRATION_GUIDE.md)
  - [Mock 服务使用指南](MOCK_SERVICE_GUIDE.md)
  - [GitHub Token 配置指南](setup-github-token.md)
- 创建新的需求并运行工作流
- 查看生成的代码和测试报告

### 步骤 1：获取 Figma Token

1. 登录 [Figma](https://www.figma.com/)
2. 进入 Settings → Personal Access Tokens
3. 创建新 Token，复制保存

### 步骤 2：配置 Token

```bash
export FIGMA_TOKEN=your_figma_token_here
```

### 步骤 3：运行测试

**方式 1：一键启动（推荐）**
```bash
bash test_figma.sh
```

**方式 2：快速测试（不需要设计稿）**
```bash
python3 test_figma_quick.py
# 选择 1 - 快速测试
```

**方式 3：完整测试（需要设计稿）**
```bash
python3 test_figma_quick.py
# 选择 2 - 完整测试
# 输入 Figma URL 和页面名称
```

**方式 4：详细功能测试**
```bash
python3 test_figma_api.py
# 选择测试项目
```

### 步骤 4：查看测试结果

测试会显示：
- ✅ 组件数量和类型
- ✅ 布局信息
- ✅ 静态资源列表
- ✅ 设计稿摘要

### 详细文档

- 📖 [Figma 集成指南](FIGMA_INTEGRATION_GUIDE.md) - 完整的集成文档
- 📖 [Figma 测试指南](FIGMA_TESTING_GUIDE.md) - 详细的测试步骤
- 📖 [Figma 测试检查清单](FIGMA_TEST_CHECKLIST.md) - 测试检查清单

## 常用命令

### GitHub 相关

```bash
# 测试 GitHub 连接
python3 test_github_connection.py

# 测试 GitHub API
python3 test_github_api_guide.py

# 查看仓库信息
python3 test_github_repo.py
```

### 需求管理

```bash
# 创建示例需求
python3 create_workflow_issue.py

# 交互式创建需求
python3 create_issue_interactive.py

# 测试需求分析
python3 test_requirement_analysis.py
```

### Figma 集成

```bash
# Figma 快速测试
python3 test_figma_quick.py

# Figma 详细测试
python3 test_figma_api.py

# 一键启动测试
bash test_figma.sh
```

### 项目管理

```bash
# 初始化 React 项目
python3 init_react_vite.py

# 连接用户仓库
python3 connect_user_repo.py

# 运行 GitHub 连接设置
bash setup_github_connection.sh
```

## 文档导航

| 文档 | 描述 |
|-----|------|
| [需求创建指南](REQUIREMENT_CREATE_GUIDE.md) | 如何创建符合格式的要求 |
| [GitHub 仓库使用指南](GITHUB_REPO_USAGE.md) | GitHub 集成使用说明 |
| [代码推送指南](GITHUB_CODE_PUSH_GUIDE.md) | 如何推送代码到 GitHub |
| [工作流能力清单](CURRENT_CAPABILITIES.md) | 当前支持的功能 |
| [AGENTS.md](AGENTS.md) | 工作流节点清单 |

## 常见问题

### Q: 如何创建一个新的需求？

A: 使用以下任一方式：
1. 运行 `python3 create_workflow_issue.py` 创建示例需求
2. 运行 `python3 create_issue_interactive.py` 交互式创建
3. 直接在 GitHub 上手动创建

### Q: 需求格式有什么要求？

A: 需求必须包含三个部分：
1. **需求描述**: 简要描述需求背景
2. **功能列表**: 编号列表，每项一个具体功能
3. **API 定义**: 格式为 `API: 方法 URL 说明`

详见 [需求创建指南](REQUIREMENT_CREATE_GUIDE.md)

### Q: 如何测试工作流？

A:
1. 创建一个需求 Issue
2. 运行 `python3 test_requirement_analysis.py` 测试需求解析
3. 查看输出确认解析结果

### Q: 工作流支持哪些功能？

A: 查看 [工作流能力清单](CURRENT_CAPABILITIES.md) 或运行 `python3 show_capabilities.sh`

### Q: 如何配置 GitHub Token？

A: 查看 [GitHub 账号设置指南](GITHUB_ACCOUNT_SETUP_GUIDE.md)

## 下一步

1. 创建一个需求 Issue
2. 测试需求分析功能
3. 查看 AGENTS.md 了解工作流结构
4. 探索源码，理解工作流实现

## 获取帮助

如果遇到问题：
1. 查看本文档和相关指南
2. 运行 `python3 show_capabilities.sh` 查看当前状态
3. 查看日志: `/app/work/logs/bypass/app.log`
