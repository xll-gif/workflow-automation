# 项目概述
- **名称**: 登录页面完整开发工作流
- **功能**: 从 MasterGo 设计稿解析到五端（iOS、Android、鸿蒙、H5、小程序）代码生成的完整自动化流程（v7.0 新增联调测试和自动修复）

### 节点清单

| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| design_parse | nodes/design_parse_node.py | agent | 解析 MasterGo 设计稿 | - | config/design_parse_cfg.json |
| asset_processing | nodes/mastergo_asset_upload_node.py | task | 上传静态资源到对象存储（Logo 使用 mock 地址） | - | - |
| component_recognition | nodes/component_recognition_node.py | agent | 识别 UI 组件并建立层次结构 | - | config/component_recognition_cfg.json |
| **pull_ios_code** | **nodes/pull_remote_code_node.py** | **task** | **拉取 iOS 代码并分析项目规则（v6.0 新增）** | **-** | **-** |
| **pull_android_code** | **nodes/pull_remote_code_node.py** | **task** | **拉取 Android 代码并分析项目规则（v6.0 新增）** | **-** | **-** |
| **pull_harmonyos_code** | **nodes/pull_remote_code_node.py** | **task** | **拉取鸿蒙代码并分析项目规则（v6.0 新增）** | **-** | **-** |
| **pull_h5_code** | **nodes/pull_remote_code_node.py** | **task** | **拉取 H5 代码并分析项目规则（v6.0 新增）** | **-** | **-** |
| **pull_miniprogram_code** | **nodes/pull_remote_code_node.py** | **task** | **拉取小程序代码并分析项目规则（v6.0 新增）** | **-** | **-** |
| ios_code_generation | nodes/ios_code_generation_node.py | agent | 生成 iOS 代码（SwiftUI） | - | config/ios_code_generation_cfg.json |
| android_code_generation | nodes/android_code_generation_node.py | agent | 生成 Android 代码（Jetpack Compose） | - | config/android_code_generation_cfg.json |
| harmonyos_code_generation | nodes/harmonyos_code_generation_node.py | agent | 生成鸿蒙代码（ArkUI） | - | config/harmonyos_code_generation_cfg.json |
| h5_code_generation | nodes/h5_code_generation_node.py | agent | 生成 H5 代码（React + TypeScript） | - | config/h5_code_generation_cfg.json |
| miniprogram_code_generation | nodes/miniprogram_code_generation_node.py | agent | 生成小程序代码（原生小程序） | - | config/miniprogram_code_generation_cfg.json |
| ios_testing | nodes/testing_node.py | agent | iOS 代码测试验证 | - | config/testing_cfg.json |
| android_testing | nodes/testing_node.py | agent | Android 代码测试验证 | - | config/testing_cfg.json |
| harmonyos_testing | nodes/testing_node.py | agent | 鸿蒙代码测试验证 | - | config/testing_cfg.json |
| h5_testing | nodes/testing_node.py | agent | H5 代码测试验证 | - | config/testing_cfg.json |
| miniprogram_testing | nodes/testing_node.py | agent | 小程序代码测试验证 | - | config/testing_cfg.json |
| **ios_integration_test** | **nodes/integration_test_node.py** | **agent** | **iOS 联调测试（Mock 数据联调）（v7.0 新增）** | **-** | **config/integration_test_cfg.json** |
| **android_integration_test** | **nodes/integration_test_node.py** | **agent** | **Android 联调测试（Mock 数据联调）（v7.0 新增）** | **-** | **config/integration_test_cfg.json** |
| **harmonyos_integration_test** | **nodes/integration_test_node.py** | **agent** | **鸿蒙联调测试（Mock 数据联调）（v7.0 新增）** | **-** | **config/integration_test_cfg.json** |
| **h5_integration_test** | **nodes/integration_test_node.py** | **agent** | **H5 联调测试（Mock 数据联调）（v7.0 新增）** | **-** | **config/integration_test_cfg.json** |
| **miniprogram_integration_test** | **nodes/integration_test_node.py** | **agent** | **小程序联调测试（Mock 数据联调）（v7.0 新增）** | **-** | **config/integration_test_cfg.json** |
| **ios_integration_fix** | **nodes/integration_fix_node.py** | **agent** | **iOS 联调问题自动修复（v7.0 新增）** | **-** | **config/integration_fix_cfg.json** |
| **android_integration_fix** | **nodes/integration_fix_node.py** | **agent** | **Android 联调问题自动修复（v7.0 新增）** | **-** | **config/integration_fix_cfg.json** |
| **harmonyos_integration_fix** | **nodes/integration_fix_node.py** | **agent** | **鸿蒙联调问题自动修复（v7.0 新增）** | **-** | **config/integration_fix_cfg.json** |
| **h5_integration_fix** | **nodes/integration_fix_node.py** | **agent** | **H5 联调问题自动修复（v7.0 新增）** | **-** | **config/integration_fix_cfg.json** |
| **miniprogram_integration_fix** | **nodes/integration_fix_node.py** | **agent** | **小程序联调问题自动修复（v7.0 新增）** | **-** | **config/integration_fix_cfg.json** |
| h5_git_push | nodes/h5_git_push_node.py | task | 推送 H5 代码到 GitHub | - | - |
| ios_git_push | nodes/ios_git_push_node.py | task | 推送 iOS 代码到 GitHub | - | - |
| android_git_push | nodes/android_git_push_node.py | task | 推送 Android 代码到 GitHub | - | - |
| harmonyos_git_push | nodes/harmonyos_git_push_node.py | task | 推送鸿蒙代码到 GitHub | - | - |
| miniprogram_git_push | nodes/miniprogram_git_push_node.py | task | 推送小程序代码到 GitHub | - | - |
| all_platforms_summary | nodes/all_platforms_summary_node.py | agent | 汇总五端开发结果 | - | config/all_platforms_summary_cfg.json |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 工具清单

| 工具名 | 文件位置 | 功能描述 |
|-------|---------|---------|
| GitPusher | src/tools/git_pusher.py | Git 推送工具，封装克隆、写入、提交、推送操作 |

## 工作流流程

```
1. 设计稿解析 (design_parse)
   ↓
2. 资源处理 (asset_processing)
   - Logo 资源使用 mock 地址
   - 其他资源上传到对象存储
   ↓
3. 组件识别 (component_recognition)
   - 识别 UI 组件
   - 建立组件层次结构
   ↓
4. 五端并行拉取现有代码（v6.0 新增）
   - pull_ios_code：拉取 iOS 代码并分析项目规则
   - pull_android_code：拉取 Android 代码并分析项目规则
   - pull_harmonyos_code：拉取鸿蒙代码并分析项目规则
   - pull_h5_code：拉取 H5 代码并分析项目规则
   - pull_miniprogram_code：拉取小程序代码并分析项目规则
   ↓
5. 五端并行代码生成（基于现有项目规则）
   ├─ iOS 代码生成 (ios_code_generation)
   ├─ Android 代码生成 (android_code_generation)
   ├─ 鸿蒙代码生成 (harmonyos_code_generation)
   ├─ H5 代码生成 (h5_code_generation)
   └─ 小程序代码生成 (miniprogram_code_generation)
   ↓
6. 五端并行测试验证
   ├─ iOS 测试 (ios_testing)
   ├─ Android 测试 (android_testing)
   ├─ 鸿蒙测试 (harmonyos_testing)
   ├─ H5 测试 (h5_testing)
   └─ 小程序测试 (miniprogram_testing)
   ↓
7. 五端并行联调测试（v7.0 新增）
   ├─ iOS 联调测试 (ios_integration_test)
   ├─ Android 联调测试 (android_integration_test)
   ├─ 鸿蒙联调测试 (harmonyos_integration_test)
   ├─ H5 联调测试 (h5_integration_test)
   └─ 小程序联调测试 (miniprogram_integration_test)
   ↓
8. 五端并行自动修复（v7.0 新增）
   ├─ iOS 自动修复 (ios_integration_fix)
   ├─ Android 自动修复 (android_integration_fix)
   ├─ 鸿蒙自动修复 (harmonyos_integration_fix)
   ├─ H5 自动修复 (h5_integration_fix)
   └─ 小程序自动修复 (miniprogram_integration_fix)
   ↓
9. 五端并行推送到 GitHub（v5.0 新增）
   ├─ H5 推送 (h5_git_push)
   ├─ iOS 推送 (ios_git_push)
   ├─ Android 推送 (android_git_push)
   ├─ 鸿蒙推送 (harmonyos_git_push)
   └─ 小程序推送 (miniprogram_git_push)
   ↓
10. 五端汇总 (all_platforms_summary)
   ↓
11. 结束
```

## 技术栈

### 核心框架
- **工作流引擎**: LangGraph
- **编程语言**: Python 3.12+
- **大语言模型**: Claude 3.5 Sonnet
- **状态管理**: Pydantic

### 设计工具集成
- **MasterGo**: MasterGo Magic MCP

### 对象存储
- **腾讯云 COS**: WPT 环境变量
- **阿里云 OSS**: 备选方案

### 代码生成技术栈

#### iOS
- **语言**: Swift
- **框架**: SwiftUI
- **最低版本**: iOS 15.0

#### Android
- **语言**: Kotlin
- **框架**: Jetpack Compose
- **最低版本**: API 24 (Android 7.0)

#### 鸿蒙
- **语言**: ArkTS
- **框架**: ArkUI
- **最低版本**: API 9

#### H5
- **语言**: TypeScript
- **框架**: Vue 3
- **UI 库**: Element Plus / Ant Design Vue

#### 小程序
- **语言**: JavaScript / TypeScript
- **框架**: 原生小程序 / Taro
- **UI 库**: Vant Weapp / uView

## 约束配置系统

各平台使用仓库约束配置系统，确保生成的代码符合平台规范：

- **iOS**: config/constraints/ios.json
- **Android**: config/constraints/android.json
- **鸿蒙**: config/constraints/harmonyos.json
- **H5**: config/constraints/h5.json
- **小程序**: config/constraints/miniprogram.json

详见：[仓库约束配置系统文档](../docs/REPOSITORY_CONSTRAINTS.md)

## 环境变量

### 必需环境变量
```bash
# GitHub
GITHUB_TOKEN=your_github_token

# 对象存储
STORAGE_BACKEND=cos  # oss 或 cos
LOGO_FIXED_URL=https://cdn.weipaitang.com/sky/resourceMan/tupianfv/image/20260303/594f688d556e4a78bd597508c9ebd709-W140H140

# 腾讯云 COS（如果使用 COS）
WPT_SCENE_NAME=wechatCx
WPT_BUSINESS_NAME=kefu
WPT_MODE=dev
WPT_TOKEN=your_token
WPT_SECRET_KEY=your_secret_key

# MasterGo
USE_MOCK_MCP=true  # true 或 false
```

### 可选环境变量
```bash
# 大语言模型（使用默认值可省略）
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=4000
```

## 测试

### 运行工作流
```bash
cd workflow-automation
python -m graphs.login_page_graph
```

### 测试约束加载器
```bash
cd workflow-automation
pytest src/tests/test_constraint_loader.py -v
```

## 开发规范

### 节点开发规范
1. 每个节点独立文件
2. 使用 `NodeInput` 和 `NodeOutput` 作为函数签名
3. 包含完整的 docstring（title, desc, integrations）
4. 使用类型注解
5. 错误处理和日志记录

### 代码风格规范
- 遵循 PEP 8 规范
- 使用类型注解
- 函数命名使用 snake_case
- 类命名使用 PascalCase
- 常量命名使用 UPPER_SNAKE_CASE

## 设计令牌系统

### 什么是设计令牌系统？
设计令牌系统是用于实现跨平台样式一致性的核心解决方案。它通过定义统一的设计规范（颜色、间距、字体等），并自动转换为各平台的特定格式，确保五端的样式保持一致。

### 核心优势
- ✅ **单一数据源**：所有样式定义在 `config/design_tokens.json` 中
- ✅ **自动转换**：各端自动转换为对应的格式（颜色、单位等）
- ✅ **易于维护**：修改一处，所有平台同步更新
- ✅ **一致性保证**：确保五端视觉效果完全一致

### 快速使用

#### 1. 查看设计令牌定义
```bash
cat config/design_tokens.json
```

#### 2. 生成各平台令牌文件
```bash
python scripts/generate_tokens.py
```

#### 3. 在代码中使用
```python
from src.utils.design_token_converter import get_converter

converter = get_converter()

# 获取颜色（自动转换为平台格式）
color_ios = converter.get_color("primary.default", "ios")      # Color(hex: "#1890ff")
color_android = converter.get_color("primary.default", "android")  # Color(0xFF1890FF)
color_h5 = converter.get_color("primary.default", "h5")        # #1890ff

# 获取间距（自动转换为平台单位）
spacing_ios = converter.get_spacing("md", "ios")      # 16pt
spacing_android = converter.get_spacing("md", "android")  # 16dp
spacing_h5 = converter.get_spacing("md", "h5")        # 16px

# 获取组件令牌
button_height = converter.get_component_token("button", "height.md", "ios")  # 40pt
```

### 平台转换示例

| 令牌 | iOS | Android | 鸿蒙 | H5 | 小程序 |
|------|-----|---------|------|-----|--------|
| `colors.primary.default` | `Color(hex: "#1890ff")` | `Color(0xFF1890FF)` | `"#1890ff"` | `#1890ff` | `#1890ff` |
| `spacing.md` | `16pt` | `16dp` | `16vp` | `16px` | `16rpx` |
| `fontSize.md` | `16pt` | `16sp` | `16vp` | `16px` | `16rpx` |
| `borderRadius.md` | `8pt` | `8dp` | `8vp` | `8px` | `8rpx` |
| `components.button.height.md` | `40pt` | `40dp` | `40vp` | `40px` | `40rpx` |

### 在代码生成节点中使用

修改代码生成节点（如 `ios_code_generation_node.py`）：

```python
from src.utils.design_token_converter import get_converter

def ios_code_generation_node(state: IOSCodeGenerationInput, config: RunnableConfig, runtime: Runtime[Context]) -> IOSCodeGenerationOutput:
    ctx = runtime.context
    converter = get_converter()

    # 获取令牌
    primary_color = converter.get_color("primary.default", "ios")
    button_height = converter.get_component_token("button", "height.md", "ios")

    # 在生成的代码中使用令牌
    code = f'''
    Button("登录") {{
        // 使用令牌确保样式一致性
    }}
    .frame(height: {button_height})
    .background({primary_color})
    '''
```

### 相关文档
- [设计令牌系统总览](../docs/DESIGN_TOKENS_SYSTEM.md)
- [设计令牌实现示例](../docs/DESIGN_TOKENS_IMPLEMENTATION.md)
- [设计令牌定义](../config/design_tokens.json)

## 常见问题

### Q: Logo 为什么使用 mock 地址？
A: 根据 Issue #2 的特殊约束，Logo 资源直接使用预定义的 mock 地址，跳过上传流程，确保 Logo 显示正确。

### Q: iOS 项目结构是什么样的？
A: iOS 项目采用标准的 Xcode 结构，详见以下文档：
- [iOS 项目结构修复报告](../docs/IOS_STRUCTURE_FIX_REPORT.md) - 初始修复
- [iOS 项目结构清理报告](../docs/IOS_STRUCTURE_CLEANUP_REPORT.md) - 清理重复文件

**最终项目结构**：
```
ios-login-app/
├── LoginApp/                           # 源代码目录
│   ├── LoginApp.swift                  # 应用入口
│   ├── ContentView.swift               # 主视图
│   ├── AuthViewModel.swift             # 认证视图模型
│   ├── Views/                          # 视图子目录
│   │   ├── LoginView.swift
│   │   └── HomeView.swift
│   ├── Assets.xcassets/                # 资源目录
│   ├── Preview Content/                # 预览资源
│   └── Info.plist
└── LoginApp.xcodeproj/                 # Xcode 项目目录（唯一）
    └── project.pbxproj
```

**关键修复**：
- ✅ 删除根目录重复文件（App.swift, AuthViewModel.swift 等）
- ✅ 删除重复的 Views 目录
- ✅ 删除嵌套的 ios-login-app 目录
- ✅ 只保留一个 Xcode 项目文件（LoginApp.xcodeproj）

### Q: 设计稿解析出来的原始内容是什么？
A: 设计稿解析节点从 MasterGo 设计稿中提取的原始内容包括：

**数据结构**：
```json
{
  "url": "设计稿URL",
  "file_id": "文件ID",
  "file_name": "文件名称",
  "components": [
    {
      "id": "组件ID",
      "name": "组件名称",
      "type": "组件类型",
      "position": {"x": 0, "y": 0, "width": 100, "height": 100},
      "style": {
        "backgroundColor": "#1890ff",
        "fontSize": 16,
        "borderRadius": 8
      }
    }
  ],
  "images": [
    {
      "id": "图片ID",
      "name": "图片名称",
      "url": "图片URL",
      "size": {"width": 100, "height": 100}
    }
  ],
  "layout": {
    "type": "vertical",
    "spacing": 16,
    "padding": {"top": 32, "bottom": 32, "left": 16, "right": 16}
  },
  "colors": {
    "primary": "#1890ff",
    "text": "#262626",
    "background": "#ffffff"
  }
}
```

**主要提取内容**：
- **components**：所有组件（按钮、输入框、文本、图片等）
- **images**：所有图片资源
- **layout**：页面布局信息
- **colors**：颜色定义

**示例文件**：
- 通用示例：`docs/assets/mastergo_parse_mock.json`
- 实际示例：`docs/assets/design_parse_real_example.json`

**详细说明**：[设计稿解析原始内容文档](../docs/DESIGN_PARSE_RAW_CONTENT.md)

### Q: 如何添加新平台？
A:
1. 在 `config/constraints/` 下创建新的平台约束配置
2. 在 `src/graphs/nodes/` 下创建新的代码生成节点
3. 在 `src/graphs/login_page_graph.py` 中添加节点和边

### Q: 如何调试工作流？
A:
1. 查看日志文件：`/app/work/logs/bypass/app.log`
2. 使用 `test_run` 工具测试工作流
3. 检查环境变量配置

### Q: Git 推送功能如何工作？
A:
1. 使用 `GitPusher` 工具封装 Git 操作（克隆、写入、提交、推送）
2. 每个平台有独立的推送节点
3. 推送节点位于测试节点之后、汇总节点之前
4. 使用统一的提交信息格式：`feat: #{issue_number} {title} - {features}`
5. 支持批量推送和结果统计

### Q: 五端代码推送结果？
A:
所有五端代码已成功推送到对应的 GitHub 仓库：
- H5: `xll-gif/h5-login-app` (3704f9cf75ee8eabf6e8cc008994b677dd24d5f1)
- iOS: `xll-gif/ios-login-app` (32fda2faf8e9c0b8b4d5239d34ded1de35b00c9f)
- Android: `xll-gif/android-login-app` (fd27b032f68f2ed1559e8c68b636a2cdb14e983b)
- 鸿蒙: `xll-gif/harmonyos-login-app` (6a23037a5ae96ead1cdb1b0707f2c3f6e91b1718)
- 小程序: `xll-gif/miniprogram-login-app` (7fa5c292c241f5733d363e3a5d5d0a3dae99478c)

详见：[推送成功报告](../docs/PUSH_SUCCESS_REPORT.md)

### Q: 样式问题如何修复？
A:
已修复五端样式问题，包括：
1. **iOS**: 修复颜色转换函数（支持 6 位和 8 位 hex），优化布局和输入框样式
2. **Android**: 修复弃用的 `android:tint`，使用 `app:tint`，优化布局和按钮样式
3. **鸿蒙**: 统一使用 vp 单位，优化布局和交互效果
4. **小程序**: 优化样式和响应式适配，添加加载动画
5. **H5**: 添加完整的 CSS reset，优化渐变背景和交互效果

样式修复提交：
- iOS: `27a14541b92afd64ecb97f70f0b88e4870d70bbc`
- Android: `38fd7d0f5e648301ed45b8604ff0d8530e5303e`
- 鸿蒙: `884df0fe8ae2a0bf2cde9d5270eb9c8719782a10`
- 小程序: `97e7dfe03b3c7f84a16c738f658762b707c86246`
- H5: `264830450b8f7385e9e9f3e3eb530e387e56a68f`

详见：[样式修复报告](../docs/STYLE_FIX_REPORT.md)

### Q: 间距和居中问题如何修复？
A:
已修复五端间距和居中问题，确保整体内容在屏幕中垂直和水平居中显示：
1. **iOS**: 使用 GeometryReader 计算屏幕高度，使用 Spacer 实现垂直居中，统一输入框和按钮高度为 50pt
2. **Android**: 使用 `android:gravity="center"` 实现居中，统一输入框和按钮高度为 50dp
3. **鸿蒙**: 使用 Blank 组件和 `justifyContent(FlexAlign.Center)` 实现居中，统一输入框和按钮高度为 50vp
4. **小程序**: 使用 flex 布局实现居中，统一输入框和按钮高度为 100rpx
5. **H5**: 使用 flex 布局实现居中，统一输入框和按钮高度为 50px

间距和居中修复提交：
- iOS: `3c82d38b8984a6e0c7b7d969ca143cc7b729b8b7`
- Android: `7a8d58c82c2abea3c51c8063163c2865c36e8fc4`
- 鸿蒙: `389fc57d890bcaa5e5684b63e04bd3ba93c0250d`
- 小程序: `3823ca53241fd6cd38e78d44c7ec0658e2248839`
- H5: `87f88616405f6838a0f77a5eb4a04c6f67e42d39`

详见：[间距和居中修复报告](../docs/SPACING_CENTER_FIX_REPORT.md)

### Q: iOS 和 Android 项目结构如何修复？
A:
已修复 iOS 和 Android 项目结构，添加完整工程文件：
1. **iOS**: 添加 LoginApp.swift、ContentView.swift、AuthViewModel.swift、Views/LoginView.swift、Views/HomeView.swift、Info.plist、LoginApp.xcodeproj/project.pbxproj
2. **Android**: 添加 build.gradle、settings.gradle、gradle.properties、app/build.gradle、AndroidManifest.xml、LoginActivity.kt、activity_login.xml、资源文件等

项目结构修复提交：
- iOS: `99ee71d72c79d141025e2a9ac0da22a583a6bd30` (7 个文件)
- Android: `35df04212be8412d7d2bfc840f19f7ef4b596ca9` (13 个文件)

详见：[项目结构修复报告](../docs/PROJECT_STRUCTURE_FIX_REPORT.md)

## 相关文档

- [仓库约束配置系统](../docs/REPOSITORY_CONSTRAINTS.md)
- [代码生成节点使用约束指南](../docs/CODE_GENERATOR_CONSTRAINTS_GUIDE.md)
- [约束系统实现总结](../docs/CONSTRAINT_SYSTEM_IMPLEMENTATION_SUMMARY.md)
- [Issue #2: 登录页面完整开发](../.github/ISSUE_TEMPLATE/issue-002-login-page.md)

## 更新日志

### v1.0.0 (2024-03-03)
- ✅ 实现仓库约束配置系统
- ✅ 创建五端约束配置文件
- ✅ 实现约束加载器工具类
- ✅ 创建组件识别节点
- ✅ 创建测试验证节点
- ✅ 创建提交到仓库节点
- ✅ 创建五端汇总节点
- ✅ 实现 Logo 特殊约束
- ✅ 创建主图编排
- ✅ 更新 AGENTS.md

## 最近修复的问题

### 2026-03-03
1. **修复 LLMClient 初始化错误**
   - 问题描述：多个节点使用错误的 LLMClient 初始化方式（`LLMClient(llm_config)`），导致 `'dict' object has no attribute 'base_model_url'` 错误
   - 解决方案：修改为 `LLMClient(ctx=ctx)`，传递 Context 参数
   - 影响节点：component_recognition, ios_code_generation, android_code_generation, harmonyos_code_generation, miniprogram_code_generation, testing, all_platforms_summary

2. **修复配置文件路径错误**
   - 问题描述：配置文件路径包含 `_llm` 后缀，但实际文件名没有该后缀
   - 解决方案：
     - 重命名配置文件（移除 `_llm` 后缀）
     - 创建缺失的 `design_parse_cfg.json`
     - 更新 login_page_graph.py 中的配置文件路径
   - 影响文件：login_page_graph.py, config/*.json

3. **修复 GraphInput 缺少 mastergo_url 字段**
   - 问题描述：design_parse_node 需要 mastergo_url，但 GraphInput 中没有该字段
   - 解决方案：在 GraphInput 中添加 mastergo_url 字段

4. **修复 H5CodeGenerationInput 的 feature_list 必填问题**
   - 问题描述：feature_list 字段为必填，但 GlobalState 中该字段可能为空
   - 解决方案：将 feature_list 字段改为可选（添加 default=[]）

5. **修复 cos_uploader.py 的 LSP 错误**
   - 问题描述：qcloud_cos SDK 的导入路径导致 LSP 检查错误
   - 解决方案：在文件顶部添加 try-except 导入逻辑，并设置 QCLOUD_COS_AVAILABLE 标志

### 工作流验证
- ✅ 设计解析节点测试通过
- ✅ 组件识别节点测试通过
- ✅ 资源上传节点测试通过
- ✅ H5 代码生成节点测试通过
- ✅ 测试验证节点测试通过
- ✅ 五端汇总节点测试通过
- ✅ Git 推送节点测试通过
- ✅ 工作流编译成功
- ⏳ 完整工作流测试进行中（需要 GitHub Token 和仓库）

## Git 推送功能（v5.0 新增）

### 功能说明
工作流新增五端代码推送功能，可以将生成的代码自动推送到对应的 GitHub 仓库。

### 推送节点
- **h5_git_push**: 推送 H5 代码到 H5 仓库
- **ios_git_push**: 推送 iOS 代码到 iOS 仓库
- **android_git_push**: 推送 Android 代码到 Android 仓库
- **harmonyos_git_push**: 推送鸿蒙代码到鸿蒙仓库
- **miniprogram_git_push**: 推送小程序代码到小程序仓库

### 推送流程
1. 克隆远程仓库到临时目录
2. 将生成的文件写入仓库对应目录
3. 提交更改（包含 Issue 编号和功能描述）
4. 推送到远程仓库
5. 清理临时目录

### 仓库配置
推送目标仓库由以下字段决定：
- `repo_owner`: GitHub 仓库所有者（默认：xll-gif）
- `h5_repo_name`: H5 仓库名称（默认：h5-login-app）
- `ios_repo_name`: iOS 仓库名称（默认：ios-login-app）
- `android_repo_name`: Android 仓库名称（默认：android-login-app）
- `harmonyos_repo_name`: 鸿蒙仓库名称（默认：harmonyos-login-app）
- `miniprogram_repo_name`: 小程序仓库名称（默认：miniprogram-login-app）

### 环境变量要求
- `GITHUB_TOKEN`: GitHub Personal Access Token（必需）
  - 获取方式：https://github.com/settings/tokens
  - 权限要求：`repo`（完整访问权限）

### 提交信息格式
```
feat: #{issue_number} {issue_title}

实现功能：{feature_list}
```

### 推送结果
每个推送节点会返回推送结果，包含：
- `success`: 推送是否成功
- `repo_url`: 仓库 URL
- `branch`: 分支名称
- `commit_hash`: 提交哈希（如果成功）
- `error`: 错误信息（如果失败）
- `files_pushed`: 推送的文件数量

### 相关文件
- **工具**: `src/tools/git_pusher.py`
- **节点**: `src/graphs/nodes/*_git_push_node.py`（5个文件）
- **状态**: `src/graphs/state.py`（GlobalState 和推送节点输入输出）
- **编排**: `src/graphs/login_page_graph.py`（添加推送节点和边）

---

## 拉取代码功能（v6.0 新增）

### 功能说明
工作流新增五端代码拉取功能，在代码生成前先拉取各平台现有代码，分析项目规则，确保生成的代码符合现有项目规范。

### 拉取节点
- **pull_ios_code**: 拉取 iOS 代码并分析项目规则
- **pull_android_code**: 拉取 Android 代码并分析项目规则
- **pull_harmonyos_code**: 拉取鸿蒙代码并分析项目规则
- **pull_h5_code**: 拉取 H5 代码并分析项目规则
- **pull_miniprogram_code**: 拉取小程序代码并分析项目规则

### 拉取流程
1. 使用 GitHub Token 克隆远程仓库到本地临时目录
2. 切换到指定分支（默认：main）
3. 分析项目结构（目录、文件组织、模块划分）
4. 提取项目规则：
   - **项目结构**（project_structure）：目录、文件组织、模块划分
   - **代码规范**（coding_standards）：命名、风格、注释
   - **组件使用**（component_usage）：组件库、自定义组件、引用方式
   - **API 集成**（api_integration）：调用方式、错误处理、数据模型
   - **样式规范**（styling）：样式方案、命名、主题
   - **测试规范**（testing）：测试框架、文件组织、覆盖率
   - **依赖管理**（dependencies）：包管理器、常用依赖、版本规范
   - **构建配置**（build_config）：构建工具、环境变量、打包配置
5. 返回分析结果

### 仓库配置
拉取目标仓库由以下字段决定：
- `repo_owner`: GitHub 仓库所有者（默认：xll-gif）
- `h5_repo_name`: H5 仓库名称（默认：h5-login-app）
- `ios_repo_name`: iOS 仓库名称（默认：ios-login-app）
- `android_repo_name`: Android 仓库名称（默认：android-login-app）
- `harmonyos_repo_name`: 鸿蒙仓库名称（默认：harmonyos-login-app）
- `miniprogram_repo_name`: 小程序仓库名称（默认：miniprogram-login-app）

### 环境变量要求
- `GITHUB_TOKEN`: GitHub Personal Access Token（必需）
  - 获取方式：https://github.com/settings/tokens
  - 权限要求：`repo`（完整访问权限）

### 拉取结果
每个拉取节点会返回拉取结果，包含：
- `success`: 拉取是否成功
- `platform`: 目标平台
- `repo_local_path`: 本地代码路径
- `project_rules`: 提取的项目规则（ProjectRules 对象）
- `project_structure`: 项目结构
- `code_files`: 代码文件列表
- `summary`: 处理摘要

### 项目规则数据结构（ProjectRules）

```python
class ProjectRules(BaseModel):
    """项目规则数据结构"""
    project_structure: Dict[str, Any] = Field(default={}, description="项目结构（目录、文件组织、模块划分）")
    coding_standards: Dict[str, Any] = Field(default={}, description="代码规范（命名、风格、注释）")
    component_usage: Dict[str, Any] = Field(default={}, description="组件使用（组件库、自定义组件、引用方式）")
    api_integration: Dict[str, Any] = Field(default={}, description="API 集成（调用方式、错误处理、数据模型）")
    styling: Dict[str, Any] = Field(default={}, description="样式规范（样式方案、命名、主题）")
    testing: Dict[str, Any] = Field(default={}, description="测试规范（测试框架、文件组织、覆盖率）")
    dependencies: Dict[str, Any] = Field(default={}, description="依赖管理（包管理器、常用依赖、版本规范）")
    build_config: Dict[str, Any] = Field(default={}, description="构建配置（构建工具、环境变量、打包配置）")
```

### 工作流变化

**v6.0 之前的工作流**：
```
组件识别 → 代码生成 → 测试 → 推送 → 汇总
```

**v6.0 的工作流**：
```
组件识别 → 拉取代码 → 代码生成 → 测试 → 推送 → 汇总
              （并行）
```

### 使用场景

1. **在现有项目基础上添加新功能**
   - 拉取现有项目代码
   - 分析项目结构和规则
   - 生成符合项目规范的新功能代码
   - 合并到现有项目

2. **确保生成的代码符合现有项目规范**
   - 拉取现有项目代码
   - 学习现有项目的编码风格
   - 生成风格一致的代码

3. **自动适应不同项目的架构**
   - 针对不同的项目，自动分析其架构
   - 生成符合该项目架构的代码

4. **代码迁移和重构**
   - 拉取旧项目代码
   - 识别需要重构的部分
   - 生成重构后的代码

### 相关文件
- **节点**: `src/graphs/nodes/pull_remote_code_node.py`
- **包装函数**: `src/graphs/login_page_graph.py`（5个包装函数）
- **状态**: `src/graphs/state.py`（PullRemoteCodeInput, PullRemoteCodeOutput, ProjectRules）
- **编排**: `src/graphs/login_page_graph.py`（添加拉取节点和边）

### v6.0 更新清单
- ✅ 在 GlobalState 中添加拉取代码结果字段（h5_pull_result, ios_pull_result 等）
- ✅ 创建 5 个拉取代码包装函数
- ✅ 在工作流编排中添加 5 个拉取代码节点
- ✅ 更新工作流边（组件识别 → 拉取代码 → 代码生成）
- ✅ 更新工作流流程说明
- ✅ 更新 AGENTS.md 文档

---

## 联调测试功能（v7.0 新增）

### 功能说明
工作流新增五端联调测试和自动修复功能，在代码测试后进行 Mock 数据联调，并自动修复发现的问题。

### 联调测试节点
- **ios_integration_test**: iOS 联调测试（Mock 数据联调）
- **android_integration_test**: Android 联调测试（Mock 数据联调）
- **harmonyos_integration_test**: 鸿蒙联调测试（Mock 数据联调）
- **h5_integration_test**: H5 联调测试（Mock 数据联调）
- **miniprogram_integration_test**: 小程序联调测试（Mock 数据联调）

### 自动修复节点
- **ios_integration_fix**: iOS 联调问题自动修复
- **android_integration_fix**: Android 联调问题自动修复
- **harmonyos_integration_fix**: 鸿蒙联调问题自动修复
- **h5_integration_fix**: H5 联调问题自动修复
- **miniprogram_integration_fix**: 小程序联调问题自动修复

### 联调测试流程

1. **分析 API 调用**
   - 识别代码中的所有 API 调用
   - 分析 API 调用的来源（axios、fetch、uni.request 等）

2. **生成 Mock 服务**
   - 根据定义生成 Mock 服务代码（MSW/Mock.js）
   - 生成 Mock 响应数据

3. **检测代码问题**
   - 检查错误处理是否完善
   - 检查加载状态是否添加
   - 检查 Mock 服务是否集成
   - 检测 API 调用与定义是否匹配

4. **自动修复问题**
   - 添加错误处理（try-catch）
   - 添加加载状态（loading）
   - 集成 Mock 服务
   - 使用 LLM 辅助修复复杂问题

5. **生成测试报告**
   - API 调用记录
   - 问题清单和严重程度
   - 修复报告
   - 性能指标

### 检测的问题类型

1. **missing_error_handling**: 缺少错误处理
   - API 调用缺少 try-catch
   - 建议：添加 try-catch 块处理异常

2. **missing_loading_state**: 缺少加载状态
   - API 调用缺少 loading 状态
   - 建议：添加 loading 状态提升用户体验

3. **missing_mock_integration**: 缺少 Mock 服务集成
   - 代码中未集成 Mock 服务
   - 建议：集成 MSW 或 Mock.js

4. **api_mismatch**: API 调用与定义不匹配
   - API 调用方式与定义不符
   - 建议：修正 API 调用

5. **response_parsing_error**: 响应解析错误
   - API 响应数据解析不正确
   - 建议：修正响应解析逻辑

### 支持的 Mock 格式

- **MSW**: Mock Service Worker（推荐用于 React/Vue）
- **Mock.js**: Mock.js（推荐用于小程序）

### 工作流变化

**v7.0 之前的工作流**：
```
组件识别 → 拉取代码 → 代码生成 → 测试 → 推送 → 汇总
```

**v7.0 的工作流**：
```
组件识别 → 拉取代码 → 代码生成 → 测试 → 联调测试 → 自动修复 → 推送 → 汇总
                                              （并行）   （并行）
```

### 使用场景

1. **Mock 数据联调**
   - 前后端分离开发
   - 后端 API 尚未开发完成
   - 使用 Mock 数据进行联调

2. **API 调用验证**
   - 验证前端代码是否能正确调用 API
   - 验证错误处理是否完善
   - 验证响应处理是否正确

3. **代码质量提升**
   - 自动检测常见问题
   - 自动修复简单问题
   - 使用 LLM 辅助修复复杂问题

4. **跨平台一致性**
   - 确保五端对同一 API 的调用一致
   - 确保五端的错误处理一致

### 相关文件
- **节点**: `src/graphs/nodes/integration_test_node.py`
- **修复节点**: `src/graphs/nodes/integration_fix_node.py`
- **包装函数**: `src/graphs/login_page_graph.py`（10个包装函数）
- **状态**: `src/graphs/state.py`（IntegrationTestInput, IntegrationTestOutput, IntegrationFixInput, IntegrationFixOutput）
- **编排**: `src/graphs/login_page_graph.py`（添加联调和修复节点和边）
- **配置文件**: `config/integration_test_cfg.json`, `config/integration_fix_cfg.json`

### v7.0 更新清单
- ✅ 在 GlobalState 中添加联调测试结果字段
- ✅ 创建 IntegrationTestInput, IntegrationTestOutput 状态类
- ✅ 创建 IntegrationFixInput, IntegrationFixOutput 状态类
- ✅ 创建 integration_test_node.py 联调节点
- ✅ 创建 integration_fix_node.py 自动修复节点
- ✅ 创建 integration_test_cfg.json 配置文件
- ✅ 创建 integration_fix_cfg.json 配置文件
- ✅ 创建 5 个联调测试包装函数
- ✅ 创建 5 个联调修复包装函数
- ✅ 在工作流编排中添加 10 个新节点（5个测试 + 5个修复）
- ✅ 更新工作流边（测试 → 联调测试 → 修复 → 推送）
- ✅ 更新工作流流程说明（v7.0）
- ✅ 更新 AGENTS.md 文档
- ✅ 实现常见问题的自动修复（错误处理、加载状态、Mock 集成）
- ✅ 使用 LLM 辅助修复复杂问题





