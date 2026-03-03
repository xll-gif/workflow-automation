# 代码审查和自动化测试指南

## 概述

本指南介绍工作流 v3.0 中新增的代码审查和自动化测试功能。

## 功能特性

### 1. 代码审查（code_review_node）

代码审查节点使用大语言模型自动审查生成的代码，确保代码质量、规范性和安全性。

#### 审查维度

- **代码规范**（Code Standards）
  - 命名规范（变量、函数、类）
  - 代码格式（缩进、空行、行长度）
  - 注释完整性
  - 代码风格一致性

- **代码质量**（Code Quality）
  - 逻辑正确性
  - 边界条件处理
  - 错误处理机制
  - 代码复杂度

- **安全性**（Security）
  - SQL 注入防护
  - XSS 攻击防护
  - CSRF 防护
  - 权限验证
  - 敏感信息保护

- **性能**（Performance）
  - 算法复杂度
  - 资源使用（内存、CPU）
  - 潜在的性能瓶颈
  - 优化建议

- **可维护性**（Maintainability）
  - 模块化程度
  - 代码可读性
  - 可扩展性
  - 重复代码

#### 输出内容

代码审查报告包含以下内容：

```json
{
  "review_summary": {
    "overall_score": 8.5,
    "total_issues": 12,
    "critical_count": 0,
    "high_count": 2,
    "medium_count": 5,
    "low_count": 5
  },
  "issues": [
    {
      "severity": "high",
      "category": "security",
      "line": 45,
      "description": "潜在的用户输入未验证",
      "suggestion": "添加输入验证逻辑"
    },
    {
      "severity": "medium",
      "category": "performance",
      "line": 78,
      "description": "循环中重复计算",
      "suggestion": "将计算结果缓存到循环外"
    }
  ],
  "summary": "代码整体质量良好，存在 2 个高优先级问题和 5 个中优先级问题需要修复。建议重点关注安全性方面的问题。"
}
```

#### 配置说明

代码审查配置文件：`config/code_review_cfg.json`

```json
{
  "config": {
    "model": "doubao-seed-2-0-pro-260215",
    "temperature": 0.3,
    "top_p": 0.7,
    "max_completion_tokens": 4000,
    "thinking": "disabled"
  },
  "tools": [],
  "sp": "你是一位资深的代码审查专家，负责审查前端代码的质量、规范性和安全性。\n\n# 角色定义\n你是一位资深的前端代码审查专家，精通 React、Vue、SwiftUI、Jetpack Compose 等前端技术栈，拥有 10 年以上代码审查经验。\n\n# 任务目标\n你的任务是审查提供的前端代码，从多个维度进行评估，并提供详细的改进建议。\n\n# 工作流上下文\n- **Input**: 前端代码文件列表和内容\n- **Process**: 按照规范、质量、安全、性能、可维护性五个维度进行审查\n- **Output**: 包含评分、问题列表、改进建议的审查报告\n\n# 约束与规则\n- 保持客观中立\n- 问题分级：critical（严重）、high（高）、medium（中）、low（低）\n- 提供具体可执行的改进建议\n- 优先关注安全性和关键质量问题\n\n# 过程\n1. 代码规范检查（命名、格式、注释）\n2. 代码质量评估（逻辑、边界、错误处理）\n3. 安全性检查（注入、权限、敏感信息）\n4. 性能分析（算法、资源、优化）\n5. 可维护性评估（模块化、可读性、可扩展性）\n\n# 输出格式\n仅返回如下格式的 JSON 对象：\n{\n  \"review_summary\": {\n    \"overall_score\": 0.0 到 10.0,\n    \"total_issues\": 0,\n    \"critical_count\": 0,\n    \"high_count\": 0,\n    \"medium_count\": 0,\n    \"low_count\": 0\n  },\n  \"issues\": [\n    {\n      \"severity\": \"critical\" | \"high\" | \"medium\" | \"low\",\n      \"category\": \"standards\" | \"quality\" | \"security\" | \"performance\" | \"maintainability\",\n      \"line\": 0,\n      \"description\": \"问题描述\",\n      \"suggestion\": \"改进建议\"\n    }\n  ],\n  \"summary\": \"审查总结\"\n}",
  "up": "请审查以下代码文件：\n\n{% for file in code_files %}\n=== 文件: {{ file.name }} ===\n{{ file.content }}\n\n{% endfor %}\n\n请按照代码规范、质量、安全性、性能、可维护性五个维度进行审查，返回审查报告。"
}
```

### 2. 自动化测试（auto_test_node）

自动化测试节点为生成的代码编写测试用例并执行测试，确保代码功能正确性。

#### 测试类型

- **单元测试**（Unit Tests）
  - 测试单个函数或组件
  - 测试边界条件
  - 测试错误处理

- **集成测试**（Integration Tests）
  - 测试组件间的交互
  - 测试 API 集成
  - 测试数据流

- **端到端测试**（E2E Tests）
  - 测试完整的用户流程
  - 测试页面跳转
  - 测试表单提交

#### 支持的测试框架

- **H5 平台**: Vitest
- **iOS 平台**: XCTest
- **Android 平台**: JUnit
- **鸿蒙平台**: Jest
- **小程序平台**: Jest

#### 输出内容

测试报告包含以下内容：

```json
{
  "test_summary": {
    "total_tests": 25,
    "passed": 23,
    "failed": 2,
    "skipped": 0,
    "coverage": 85.5
  },
  "test_files": [
    {
      "name": "LoginForm.test.tsx",
      "tests": 5,
      "passed": 5,
      "failed": 0
    },
    {
      "name": "APIService.test.ts",
      "tests": 10,
      "passed": 8,
      "failed": 2
    }
  ],
  "failed_tests": [
    {
      "test_name": "should handle network error",
      "file": "APIService.test.ts",
      "error": "TimeoutError: Request timeout"
    }
  ],
  "summary": "测试通过率 92%，覆盖率 85.5%。存在 2 个失败的测试用例，需要修复。"
}
```

#### 配置说明

自动化测试配置文件：`config/auto_test_cfg.json`

```json
{
  "config": {
    "model": "doubao-seed-2-0-pro-260215",
    "temperature": 0.5,
    "top_p": 0.7,
    "max_completion_tokens": 4000,
    "thinking": "disabled"
  },
  "tools": [],
  "sp": "你是一位资深的测试工程师，负责为前端代码编写自动化测试用例。\n\n# 角色定义\n你是一位资深的前端测试工程师，精通 Vitest、Jest、XCTest 等测试框架，拥有 10 年以上自动化测试经验。\n\n# 任务目标\n你的任务是为提供的前端代码编写全面的测试用例，并生成测试报告。\n\n# 工作流上下文\n- **Input**: 前端代码文件列表和内容\n- **Process**: 编写单元测试、集成测试、端到端测试\n- **Output**: 测试文件列表、测试结果、覆盖率统计\n\n# 约束与规则\n- 测试覆盖率 ≥ 80%\n- 测试用例包含正常场景和异常场景\n- H5 平台使用 Vitest\n- 保持测试代码简洁易读\n\n# 过程\n1. 分析代码结构，确定需要测试的功能点\n2. 编写单元测试（覆盖核心功能）\n3. 编写集成测试（测试组件交互）\n4. 编写端到端测试（测试完整流程）\n5. 生成测试报告和覆盖率统计\n\n# 输出格式\n仅返回如下格式的 JSON 对象：\n{\n  \"test_files\": [\n    {\n      \"name\": \"文件名\",\n      \"content\": \"测试文件内容\"\n    }\n  ],\n  \"test_summary\": {\n    \"total_tests\": 0,\n    \"passed\": 0,\n    \"failed\": 0,\n    \"skipped\": 0,\n    \"coverage\": 0.0\n  },\n  \"summary\": \"测试总结\"\n}",
  "up": "请为以下代码文件编写测试用例：\n\n{% for file in code_files %}\n=== 文件: {{ file.name }} ===\n{{ file.content }}\n\n{% endfor %}\n\n平台: {{ platform }}\n\n请编写单元测试、集成测试和端到端测试，返回测试文件和测试报告。"
}
```

## 工作流集成

### 执行流程

代码审查和自动化测试节点在工作流中的位置：

```
五端代码生成
    ↓
代码收集（fetch_generated_code）
    ↓
[代码审查 + 自动化测试] ⚡ 并行执行
    ├─ code_review（代码审查）
    └─ auto_test（自动化测试）
    ↓
GitHub 推送（code_gen_and_push）
```

### 并行执行优势

代码审查和自动化测试并行执行，可以显著提升效率：

- **串行执行**：审查（30s）+ 测试（30s）= 60s
- **并行执行**：max(30s, 30s）≈ 35s
- **效率提升**：约 1.7倍

## 使用示例

### 1. 查看代码审查报告

工作流完成后，代码审查报告保存在 `assets/code_review_report.json`：

```bash
cat assets/code_review_report.json
```

### 2. 查看测试报告

测试报告保存在 `assets/test_report.json`：

```bash
cat assets/test_report.json
```

### 3. 运行 H5 测试

进入 H5 项目目录：

```bash
cd repos/h5-login-app
npm install
npm run test
```

### 4. 查看测试覆盖率

```bash
npm run test:coverage
```

## 最佳实践

### 1. 代码审查

- **优先级**：critical > high > medium > low
- **重点关注**：安全性 > 功能性 > 性能 > 可维护性
- **修复建议**：提供具体可执行的改进建议
- **审查频率**：每次代码生成后自动执行

### 2. 自动化测试

- **测试覆盖率**：≥ 80%
- **测试类型**：单元测试 + 集成测试 + 端到端测试
- **测试命名**：清晰描述测试场景
- **测试数据**：使用 Mock 数据，避免依赖真实环境

### 3. 持续改进

- **定期更新审查规则**：根据项目规范调整审查维度
- **优化测试用例**：根据实际使用情况调整测试策略
- **分析失败原因**：记录并分析失败用例的根本原因

## 常见问题

### Q: 代码审查失败怎么办？

A: 查看代码审查报告，优先修复 critical 和 high 级别的问题。修复后重新运行工作流。

### Q: 测试覆盖率低怎么办？

A: 检查测试报告，识别未覆盖的代码路径，补充测试用例。

### Q: 测试失败怎么处理？

A: 查看失败的测试用例和错误信息，修复代码或调整测试逻辑。

### Q: 如何自定义审查规则？

A: 修改 `config/code_review_cfg.json` 中的 `sp`（系统提示词），调整审查维度和规则。

### Q: 如何添加自定义测试用例？

A: 在测试报告中查看生成的测试文件，手动添加自定义测试用例。

## 配置文件

- `config/code_review_cfg.json` - 代码审查配置
- `config/auto_test_cfg.json` - 自动化测试配置

## 相关文档

- [工作流快速开始指南](QUICK_START.md)
- [Mock 服务使用指南](MOCK_SERVICE_GUIDE.md)
- [项目更新日志](../CHANGELOG.md)
