# 工作流缓存问题解决指南

## 问题描述

平台预览显示的工作流是旧的简化版（10个节点），而不是实际 `graph.py` 中的完整五端工作流（34个节点）。

## 解决方法

### 方法 1：刷新项目（推荐）

在 Coze Coding 平台上：

1. **刷新浏览器页面**
   - 按 `Ctrl + F5`（Windows）或 `Cmd + Shift + R`（Mac）
   - 强制刷新页面，清除浏览器缓存

2. **重新加载项目**
   - 在项目列表中，点击"刷新"按钮
   - 或者退出项目后重新进入

3. **清理项目缓存**
   - 在项目设置中找到"缓存清理"选项
   - 点击清理缓存后重新加载

### 方法 2：验证本地工作流

在本地终端运行预览工具，确认工作流是否正确：

```bash
# 清理 Python 缓存
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# 运行预览工具
python scripts/preview_workflow.py
```

**应该看到**：
- 34 个节点
- 包含五端并行分支（iOS、Android、鸿蒙、H5、小程序）
- 包含联调测试和自动修复节点

### 方法 3：检查平台配置

如果平台仍然显示旧的工作流，请检查：

1. **确认工作流文件**
   - 确保 `src/graphs/graph.py` 是最新的（450 行）
   - 检查文件修改时间是否为最新

2. **确认环境变量**
   - 检查 `.env` 文件是否配置正确
   - 确保没有覆盖 `graph.py` 的路径配置

3. **确认 Git 状态**
   ```bash
   git log --oneline -5
   ```
   应该看到最近的提交：
   ```
   e95f348 docs: 更新 README.md，添加工作流预览说明
   ad6b0a0 feat: 添加工作流预览工具
   f21a17c feat: 将完整的登录页面五端工作流设为默认工作流
   ```

### 方法 4：重新部署（如果需要）

如果以上方法都无效，可能需要重新部署项目：

1. **确认所有更改已提交**
   ```bash
   git status
   ```
   应该显示：`On branch main`，且没有未提交的更改

2. **推送最新代码**
   ```bash
   git push origin main
   ```

3. **在平台重新部署**
   - 在 Coze Coding 平台上点击"重新部署"
   - 或使用"重新加载工作流"功能

## 期望的工作流

完整的五端工作流应该包含：

### 节点数量：34 个

```
1. design_parse（设计稿解析）
2. asset_processing（资源处理）
3. component_recognition（组件识别）

4-8. 五端代码拉取（5个节点）
   - pull_ios_code
   - pull_android_code
   - pull_harmonyos_code
   - pull_h5_code
   - pull_miniprogram_code

9-13. 五端代码生成（5个节点）
   - ios_code_generation
   - android_code_generation
   - harmonyos_code_generation
   - h5_code_generation
   - miniprogram_code_generation

14-18. 五端测试验证（5个节点）
   - ios_testing
   - android_testing
   - harmonyos_testing
   - h5_testing
   - miniprogram_testing

19-23. 五端联调测试（5个节点）
   - ios_integration_test
   - android_integration_test
   - harmonyos_integration_test
   - h5_integration_test
   - miniprogram_integration_test

24-28. 五端自动修复（5个节点）
   - ios_integration_fix
   - android_integration_fix
   - harmonyos_integration_fix
   - h5_integration_fix
   - miniprogram_integration_fix

29-33. 五端 Git 推送（5个节点）
   - ios_git_push
   - android_git_push
   - harmonyos_git_push
   - h5_git_push
   - miniprogram_git_push

34. all_platforms_summary（五端汇总）
```

### 执行流程

```
开始
  ↓
设计稿解析
  ↓
资源处理
  ↓
组件识别
  ↓
五端并行代码拉取（iOS、Android、鸿蒙、H5、小程序）
  ↓
五端并行代码生成
  ↓
五端并行测试验证
  ↓
五端并行联调测试
  ↓
五端并行自动修复
  ↓
五端并行 Git 推送
  ↓
五端汇总
  ↓
结束
```

## 临时解决方案

如果平台暂时无法正确加载完整工作流，您可以使用以下方式预览：

### 1. 使用本地预览工具

```bash
python scripts/preview_workflow.py
```

### 2. 查看 Mermaid 流程图

预览工具会生成 Mermaid 格式的流程图代码，您可以：
- 复制到 Markdown 文件中
- 使用 [Mermaid Live Editor](https://mermaid.live/) 在线查看

### 3. 查看文档

- `AGENTS.md` - 完整的节点清单
- `README.md` - 项目说明和工作流流程

## 联系支持

如果以上方法都无法解决问题，请：

1. 截图显示当前的工作流
2. 提供错误日志（如果有）
3. 提交 GitHub Issue：https://github.com/xll-gif/workflow-automation/issues
