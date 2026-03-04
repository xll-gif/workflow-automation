# 企业前端工程师自动化工作流 - 项目结构索引

## 项目概述
- **名称**: Frontend Automation Workflow（企业前端工程师自动化工作流）
- **功能**: 基于大模型与自动化工具，实现从需求文档和设计稿到 H5 代码的自动生成、静态资源管理与组件识别
- **核心能力**: 需求分析、设计稿解析、静态资源处理、组件识别、H5 代码生成
- **设计工具**: MasterGo（通过官方 Magic MCP 集成）
- **存储后端**: 阿里云 OSS / 腾讯云 COS（支持 STS 临时凭证）

### 节点清单

| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 | 备注 |
|-------|---------|------|---------|---------|---------|------|
| requirement_analysis_node | `src/graphs/nodes/requirement_analysis_node.py` | agent | 需求分析，解析 GitHub Issue 内容 | - | `config/requirement_analysis_cfg.json` | 支持降级策略 |
| design_parse_node | `src/graphs/nodes/design_parse_node.py` | task | 解析 MasterGo 设计稿 | - | - | 使用 MasterGo Magic MCP |
| extract_assets_node | `src/graphs/nodes/extract_assets_node.py` | task | 从设计稿提取静态资源 | - | - | 静态资源处理流程第1步 |
| optimize_assets_node | `src/graphs/nodes/optimize_assets_node.py` | task | 资源分类和优化 | - | - | 静态资源处理流程第2步 |
| upload_assets_node | `src/graphs/nodes/upload_assets_node.py` | task | 上传资源到对象存储（阿里云OSS/腾讯云COS/Mock） | - | - | 静态资源处理流程第3步 |
| generate_asset_mapping_node | `src/graphs/nodes/generate_asset_mapping_node.py` | task | 生成资源映射表 | - | - | 静态资源处理流程第4步 |
| component_identify_node | `src/graphs/nodes/component_identify_node.py` | agent | 识别设计稿中的组件 | - | `config/component_identify_cfg.json` | 使用多模态大模型 |
| h5_code_generation_node | `src/graphs/nodes/h5_code_generation_node.py` | agent | 生成 H5 代码（React + TypeScript + Vite） | - | `config/h5_code_generation_cfg.json` | 支持静态资源本地化 |
| hello_world_node | `src/graphs/nodes/hello_world_node.py` | task | Hello World 测试节点 | - | - | 测试用 |
| analyze_codebase_node | `src/graphs/nodes/analyze_codebase_node.py` | task | 分析代码库 | - | - | 代码分析 |
| code_gen_and_push_node | `src/graphs/nodes/code_gen_and_push_node.py` | task | 代码生成并推送 | - | - | 代码推送 |
| mastergo_asset_upload_node | `src/graphs/nodes/mastergo_asset_upload_node.py` | task | 上传 MasterGo 资源到对象存储 | - | - | 已废弃，被新流程替代 |
| mock_service_generator_node | `src/graphs/nodes/mock_service_generator_node.py` | task | 生成 Mock 服务 | - | - | Mock 数据生成 |

**类型说明**: task(任务节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

### 子图清单

| 子图名 | 文件位置 | 功能描述 | 被调用节点 | 循环类型 |
|-------|---------|------|---------|---------|
| - | - | - | - | - |

**说明**: 当前工作流未使用子图，所有节点在主图中编排

### 技能使用

- **大语言模型**:
  - requirement_analysis_node - 需求分析（解析 GitHub Issue 内容）
  - component_identify_node - 组件识别（使用多模态大模型识别设计稿）
  - h5_code_generation_node - H5 代码生成（生成 React + TypeScript + Vite 完整应用）

- **MasterGo 集成**:
  - design_parse_node - 解析 MasterGo 设计稿（使用官方 Magic MCP）
  - mastergo_asset_upload_node - 上传 MasterGo 资源到对象存储（已废弃）

- **对象存储**:
  - upload_assets_node - 上传静态资源（支持阿里云 OSS / 腾讯云 COS / Mock）

### 工具清单

| 工具名 | 文件位置 | 功能描述 | 使用节点 |
|-------|---------|---------|---------|
| GitHub API Client | `src/tools/github_api_client.py` | GitHub API 客户端 | requirement_analysis_node |
| MasterGo MCP Client | `src/tools/mastergo_mcp_client.py` | MasterGo Magic MCP 客户端 | design_parse_node |
| MasterGo Asset Uploader | `src/tools/mastergo_asset_uploader.py` | MasterGo 资产上传器 | mastergo_asset_upload_node |
| TencentCOSUploader | `src/tools/cos_uploader.py` | 腾讯云 COS 上传工具（支持 STS 临时凭证） | upload_assets_node |

### 配置文件清单

| 配置文件 | 位置 | 用途 |
|---------|------|------|
| requirement_analysis_cfg.json | `config/requirement_analysis_cfg.json` | 需求分析大模型配置 |
| component_identify_cfg.json | `config/component_identify_cfg.json` | 组件识别大模型配置 |
| h5_code_generation_cfg.json | `config/h5_code_generation_cfg.json` | H5 代码生成大模型配置 |
| mastergo_config.json | `config/mastergo_config.json` | MasterGo API 配置（API URL、MCP Token 等） |

### 数据结构

#### 全局状态 (GlobalState)
- `input_message`: 输入消息
- `output_message`: 输出消息
- `processing_time`: 处理耗时（秒）
- `github_issue_url`: GitHub Issue URL
- `issue_title`: Issue 标题
- `issue_body`: Issue 内容
- `feature_list`: 功能列表
- `api_definitions`: API 定义列表
- `mastergo_url`: MasterGo 设计稿 URL
- `components`: UI 组件列表
- `layout`: 布局信息
- `static_assets`: 静态资源列表
- `mastergo_summary`: 设计稿摘要
- `raw_assets`: 提取的原始资源列表
- `optimized_assets`: 优化后的资源列表
- `categorized_assets`: 分类后的资源
- `uploaded_assets`: 上传成功的资源列表
- `asset_mapping`: 资源映射表（组件名 → OSS URL）
- `identified_components`: 识别后的组件列表
- `component_hierarchy`: 组件层次结构
- `design_summary`: 设计摘要
- `suggestions`: 设计建议
- `h5_generated_files`: H5 生成的文件列表
- `h5_generation_summary`: H5 代码生成摘要

#### 工作流输入 (GraphInput)
- `input_message`: 输入消息
- `github_issue_url`: GitHub Issue URL
- `issue_title`: Issue 标题
- `issue_body`: Issue 内容

#### 工作流输出 (GraphOutput)
- `output_message`: 输出消息
- `processing_time`: 处理耗时（秒）
- `feature_list`: 功能列表
- `api_definitions`: API 定义列表
- `mastergo_url`: MasterGo 设计稿 URL
- `components`: UI 组件列表
- `layout`: 布局信息
- `static_assets`: 静态资源列表
- `mastergo_summary`: 设计稿摘要
- `identified_components`: 识别后的组件列表
- `component_hierarchy`: 组件层次结构
- `design_summary`: 设计摘要
- `suggestions`: 设计建议
- `h5_generated_files`: H5 生成的文件列表
- `h5_generation_summary`: H5 代码生成摘要

### 文档清单

| 文档名 | 位置 | 用途 |
|-------|------|------|
| README.md | `README.md` | 项目说明文档 |
| AGENTS.md | `AGENTS.md` | 本文件，项目结构索引 |
| ENVIRONMENT_VARIABLES.md | `ENVIRONMENT_VARIABLES.md` | 环境变量配置指南 |
| TENCENT_COS_INTEGRATION_GUIDE.md | `TENCENT_COS_INTEGRATION_GUIDE.md` | 腾讯云 COS 集成指南 |
| STATIC_ASSET_PROCESSING_GUIDE.md | `STATIC_ASSET_PROCESSING_GUIDE.md` | 静态资源处理完整指南 |
| WPTRESOURCE_ANALYSIS.md | `WPTRESOURCE_ANALYSIS.md` | wptresource 仓库代码分析报告 |
| .env.tencentyun.example | `.env.tencentyun.example` | 腾讯云 COS 客户端配置文件示例 |

### 服务清单

| 服务名 | 文件位置 | 功能描述 | 依赖 |
|-------|---------|---------|------|
| Tencent COS API Server | `api_server.py` | 提供获取 STS 临时凭证的 API 服务 | Flask, 腾讯云 STS SDK |

### 关键技术栈

- **工作流框架**: LangGraph
- **编程语言**: Python 3.9+
- **需求管理**: GitHub Issues
- **设计工具**: MasterGo（通过官方 Magic MCP 集成）
- **对象存储**: 阿里云 OSS / 腾讯云 COS（支持 STS 临时凭证）
- **模型能力**: 多模态大模型（设计稿识别）、代码生成大模型
- **前端技术栈**: React 18 + TypeScript + Vite + React Router + Axios

### 工作流流程

```
开始
  ↓
需求分析（requirement_analysis）
  ↓
解析设计稿（design_parse）
  ↓
提取静态资源（extract_assets）
  ↓
优化静态资源（optimize_assets）
  ↓
上传资源到对象存储（upload_assets）
  ↓
生成资源映射表（generate_asset_mapping）
  ↓
识别组件（component_identify）
  ↓
生成 H5 代码（h5_code_generation）
  ↓
结束
```

### 工作流说明

**当前工作流实现的功能**：
1. 从 GitHub Issue 解析需求文档
2. 解析 MasterGo 设计稿获取设计信息
3. 从设计稿提取静态资源（图片、图标、字体等）
4. 对静态资源进行分类和优化（格式转换、尺寸优化等）
5. 将静态资源上传到对象存储（支持阿里云 OSS / 腾讯云 COS / Mock 模式）
6. 生成资源映射表，将组件名映射到资源 URL
7. 使用多模态大模型识别设计稿中的组件
8. 生成 H5 代码（React + TypeScript + Vite）

**技术特点**：
- 支持降级策略（API 限流时使用备用方案）
- 支持静态资源本地化（资源 URL 写入代码中）
- 支持多种对象存储后端（阿里云 OSS / 腾讯云 COS / Mock）
- 使用 MasterGo 官方 Magic MCP 进行设计稿解析
- 使用多模态大模型进行组件识别

**未来扩展计划**：
- 添加 iOS、Android、鸿蒙、小程序代码生成节点
- 添加 API 规范生成节点
- 添加测试执行节点
- 添加代码提交到 GitHub 节点
- 添加人工审核节点
