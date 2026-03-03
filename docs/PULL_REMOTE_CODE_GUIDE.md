# 远程代码拉取和同步指南

## 概述

本文档介绍如何使用工作流拉取远程代码并基于现有代码生成符合项目规范的新代码。

## 功能说明

### v4.0 新增功能

工作流 v4.0 新增了**项目规则解析**功能，在生成代码之前会分析各平台项目的编码规范和最佳实践。

### 支持的拉取方式

1. **GitHub API 分析**（推荐）
   - 使用 GitHub API 读取远程仓库的文件内容
   - 无需下载完整代码
   - 速度快，资源占用少

2. **Git 克隆分析**（完整功能）
   - 使用 `git clone` 拉取完整代码到本地
   - 基于本地代码深度分析
   - 支持复杂的项目结构分析

## 使用步骤

### 步骤 1：配置 GitHub Token

```bash
export GITHUB_TOKEN="your_github_token_here"
```

**注意**：GitHub Token 需要有 `repo` 权限才能读取私有仓库。

### 步骤 2：创建各平台仓库

在工作流执行前，先在 GitHub 上创建各平台的仓库：

```bash
# H5 仓库
https://github.com/xll-gif/h5-login-app

# iOS 仓库
https://github.com/xll-gif/ios-login-app

# Android 仓库
https://github.com/xll-gif/android-login-app

# 鸿蒙仓库
https://github.com/xll-gif/harmonyos-login-app

# 小程序仓库
https://github.com/xll-gif/miniprogram-login-app
```

### 步骤 3：初始化各平台项目

#### H5 项目（React + TypeScript + Vite）

```bash
# 在本地初始化 H5 项目
npm create vite@latest h5-login-app -- --template react-ts
cd h5-login-app
npm install

# 安装常用依赖
npm install antd axios react-router-dom zustand
npm install -D @types/node vitest eslint prettier

# 提交到 GitHub
git init
git add .
git commit -m "Initial commit: H5 project setup"
git branch -M main
git remote add origin https://github.com/xll-gif/h5-login-app.git
git push -u origin main
```

#### iOS 项目（SwiftUI）

```bash
# 在本地创建 Xcode 项目
# File > New > Project > iOS > App

# 提交到 GitHub
cd ios-login-app
git init
git add .
git commit -m "Initial commit: iOS project setup"
git remote add origin https://github.com/xll-gif/ios-login-app.git
git push -u origin main
```

#### Android 项目（Jetpack Compose）

```bash
# 使用 Android Studio 创建项目
# File > New > New Project > Phone and Tablet > Empty Activity

# 提交到 GitHub
cd android-login-app
git init
git add .
git commit -m "Initial commit: Android project setup"
git remote add origin https://github.com/xll-gif/android-login-app.git
git push -u origin main
```

#### 鸿蒙项目（ArkTS）

```bash
# 使用 DevEco Studio 创建项目

# 提交到 GitHub
cd harmonyos-login-app
git init
git add .
git commit -m "Initial commit: HarmonyOS project setup"
git remote add origin https://github.com/xll-gif/harmonyos-login-app.git
git push -u origin main
```

#### 小程序项目

```bash
# 使用微信开发者工具创建项目

# 提交到 GitHub
cd miniprogram-login-app
git init
git add .
git commit -m "Initial commit: Miniprogram project setup"
git remote add origin https://github.com/xll-gif/miniprogram-login-app.git
git push -u origin main
```

### 步骤 4：运行工作流

```bash
python src/main.py
```

**输入参数**：

```json
{
  "github_issue_url": "https://github.com/xll-gif/workflow-automation/issues/1",
  "repo_owner": "xll-gif",
  "h5_repo_name": "h5-login-app",
  "ios_repo_name": "ios-login-app",
  "android_repo_name": "android-login-app",
  "harmonyos_repo_name": "harmonyos-login-app",
  "miniprogram_repo_name": "miniprogram-login-app"
}
```

### 步骤 5：查看生成的代码

工作流执行完成后，会自动将生成的代码推送到各平台仓库：

```bash
# H5 仓库
https://github.com/xll-gif/h5-login-app

# iOS 仓库
https://github.com/xll-gif/ios-login-app

# Android 仓库
https://github.com/xll-gif/android-login-app

# 鸿蒙仓库
https://github.com/xll-gif/harmonyos-login-app

# 小程序仓库
https://github.com/xll-gif/miniprogram-login-app
```

## 工作流程

```
开始
  ↓
1. 需求分析（GitHub Issues）
  ↓
2. 设计稿解析（MasterGo）
  ↓
3. 静态资源上传（OSS）
  ↓
4. 组件识别（AI）
  ↓
5. [五端项目规则解析] ⭐ 新增
  ├─ H5 项目规则解析（分析 package.json、tsconfig.json 等）
  ├─ iOS 项目规则解析（分析 Package.swift、Info.plist 等）
  ├─ Android 项目规则解析（分析 build.gradle 等）
  ├─ 鸿蒙项目规则解析（分析 oh-package.json5 等）
  └─ 小程序项目规则解析（分析 app.json 等）
  ↓
6. [五端代码生成]（基于项目规则）
  ↓
7. 代码收集
  ↓
8. [代码审查 + 测试]
  ↓
9. 推送到 GitHub
  ↓
结束
```

## 项目规则解析维度

### 1. 项目结构（Project Structure）
- 目录组织方式
- 文件命名规范
- 模块划分方式

### 2. 代码规范（Coding Standards）
- 命名规范
- 代码风格（缩进、引号、分号等）
- 注释规范
- Lint 规则
- Formatter 配置

### 3. 组件使用（Component Usage）
- UI 框架
- 组件库
- 自定义组件
- 组件引用方式

### 4. API 集成（API Integration）
- HTTP 客户端
- 基础 URL 配置
- 请求/响应拦截器
- 错误处理方式

### 5. 样式规范（Styling）
- 样式方案
- 样式命名规范
- 响应式设计
- 主题配置

### 6. 测试规范（Testing）
- 测试框架
- 测试文件组织
- 测试覆盖率要求

### 7. 依赖管理（Dependencies）
- 包管理器
- 常用依赖
- 版本规范

### 8. 构建配置（Build Configuration）
- 构建工具
- 环境变量
- 打包配置

## 代码生成示例

### H5 代码（基于项目规则）

**输入**：
- 项目规则：使用 Ant Design 组件库、Axios 请求库、CSS Modules 样式方案

**输出**：
```tsx
// src/components/LoginForm.tsx
import React, { useState } from 'react';
import { Form, Input, Button } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import axios from 'axios';

interface LoginFormProps {
  onSuccess: (token: string) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false);

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/auth/login', {
        email: values.email,
        password: values.password,
      });
      onSuccess(response.data.token);
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form onFinish={onFinish}>
      <Form.Item name="email" rules={[{ required: true }]}>
        <Input prefix={<UserOutlined />} placeholder="Email" />
      </Form.Item>
      <Form.Item name="password" rules={[{ required: true }]}>
        <Input.Password prefix={<LockOutlined />} placeholder="Password" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading} block>
          Login
        </Button>
      </Form.Item>
    </Form>
  );
};

export default LoginForm;
```

### iOS 代码（基于项目规则）

**输入**：
- 项目规则：使用 SwiftUI、MVVM 架构、Combine 框架

**输出**：
```swift
// Views/LoginView.swift
import SwiftUI
import Combine

struct LoginView: View {
    @StateObject private var viewModel = LoginViewModel()
    
    var body: some View {
        VStack(spacing: 20) {
            TextField("Email", text: $viewModel.email)
                .textFieldStyle(RoundedBorderTextFieldStyle())
            
            SecureField("Password", text: $viewModel.password)
                .textFieldStyle(RoundedBorderTextFieldStyle())
            
            Button(action: {
                viewModel.login()
            }) {
                Text("Login")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            .disabled(viewModel.isLoading)
        }
        .padding()
    }
}

// ViewModels/LoginViewModel.swift
import Foundation
import Combine

class LoginViewModel: ObservableObject {
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var isLoading: Bool = false
    @Published var errorMessage: String = ""
    
    private var cancellables = Set<AnyCancellable>()
    
    func login() {
        isLoading = true
        
        // API 调用
        APIService.shared.login(email: email, password: password)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    self.isLoading = false
                    if case .failure(let error) = completion {
                        self.errorMessage = error.localizedDescription
                    }
                },
                receiveValue: { token in
                    // 登录成功处理
                    self.isLoading = false
                    AppManager.shared.saveToken(token)
                }
            )
            .store(in: &cancellables)
    }
}
```

## 常见问题

### Q1: 如何确保生成的代码符合现有项目规范？

A: 工作流会先分析现有项目的配置文件（如 package.json、tsconfig.json、.eslintrc 等），提取项目规范，然后基于这些规范生成代码。

### Q2: 如果仓库是私有的怎么办？

A: 确保 GitHub Token 有 `repo` 权限，并设置环境变量 `GITHUB_TOKEN`。

### Q3: 如何增量更新代码，而不是全量生成？

A: 当前版本支持全量生成。如果需要增量更新，可以在代码生成节点中指定只生成特定文件。

### Q4: 生成的代码如何与现有代码合并？

A: 当前版本会在新分支生成代码，然后创建 Pull Request。你可以手动审查并合并到主分支。

### Q5: 支持哪些代码版本管理工具？

A: 目前支持 GitHub（Git）。未来计划支持 GitLab、Bitbucket 等。

## 最佳实践

### 1. 统一代码规范
- 在各平台仓库中配置统一的代码规范（ESLint、Prettier 等）
- 使用 pre-commit hooks 确保代码质量

### 2. 模块化项目结构
- 按功能模块组织代码
- 保持一致的目录结构

### 3. 文档化
- 在 README 中说明项目结构
- 添加代码注释说明复杂逻辑

### 4. 持续集成
- 使用 GitHub Actions 自动化测试
- 确保每次提交都通过测试

### 5. 版本管理
- 使用语义化版本号
- 保持 CHANGELOG 更新

## 后续优化方向

- [ ] 支持增量代码生成
- [ ] 支持代码冲突自动解决
- [ ] 支持多仓库管理
- [ ] 支持代码审查集成
- [ ] 支持自动化测试触发
- [ ] 支持部署自动化
