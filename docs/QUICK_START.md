# 快速开始指南

## iOS 项目快速开始

### 1. 克隆项目
```bash
git clone https://github.com/xll-gif/ios-login-app.git
cd ios-login-app
```

### 2. 打开项目
```bash
open LoginApp.xcodeproj
```

### 3. 选择模拟器
在 Xcode 顶部工具栏中选择目标设备（推荐 iPhone 15 Pro）

### 4. 运行项目
点击 Xcode 左上角的 ▶ 按钮，或按 `Cmd + R`

### 5. 测试登录
- 用户名: `admin`
- 密码: `123456`

---

## Android 项目快速开始

### 1. 克隆项目
```bash
git clone https://github.com/xll-gif/android-login-app.git
cd android-login-app
```

### 2. 打开项目
在 Android Studio 中：
```
File -> Open -> 选择项目目录
```

### 3. 同步 Gradle
Android Studio 会自动提示同步 Gradle，点击 "Sync Now"

### 4. 选择模拟器
在 Android Studio 顶部工具栏中选择目标设备（推荐 Pixel 6）

### 5. 运行项目
点击 Android Studio 顶部的 ▶ 按钮，或按 `Shift + F10`

### 6. 测试登录
- 用户名: `admin`
- 密码: `123456`

---

## 鸿蒙项目快速开始

### 1. 克隆项目
```bash
git clone https://github.com/xll-gif/harmonyos-login-app.git
cd harmonyos-login-app
```

### 2. 打开项目
使用 DevEco Studio 打开项目

### 3. 选择模拟器
在 DevEco Studio 中选择目标设备

### 4. 运行项目
点击 DevEco Studio 顶部的 ▶ 按钮

### 5. 测试登录
- 用户名: `admin`
- 密码: `123456`

---

## 小程序项目快速开始

### 1. 克隆项目
```bash
git clone https://github.com/xll-gif/miniprogram-login-app.git
cd miniprogram-login-app
```

### 2. 导入项目
使用微信开发者工具：
```
文件 -> 导入项目 -> 选择项目目录
```

### 3. 预览项目
点击微信开发者工具顶部的 "预览" 按钮

### 4. 测试登录
- 用户名: `admin`
- 密码: `123456`

---

## H5 项目快速开始

### 1. 克隆项目
```bash
git clone https://github.com/xll-gif/h5-login-app.git
cd h5-login-app
```

### 2. 安装依赖
```bash
npm install
```

### 3. 运行项目
```bash
npm run dev
```

### 4. 访问应用
在浏览器中打开：http://localhost:3000

### 5. 测试登录
- 用户名: `admin`
- 密码: `123456`

---

## 常见问题

### iOS 常见问题

**Q: Xcode 报错 "Signing for xxx requires a development team"**
A: 在 Xcode 项目设置中设置 Development Team

**Q: 模拟器无法启动**
A: 重启 Xcode 或更换其他模拟器

**Q: 构建失败**
A: 清理构建文件夹（Product -> Clean Build Folder）

### Android 常见问题

**Q: Gradle 同步失败**
A: 检查网络连接，或使用国内镜像源

**Q: 模拟器无法启动**
A: 检查 HAXM 是否正确安装

**Q: 构建失败**
A: Clean Project (Build -> Clean Project)

### 鸿蒙常见问题

**Q: DevEco Studio 无法打开项目**
A: 检查 DevEco Studio 版本是否兼容

**Q: 构建失败**
A: Clean Project (Build -> Clean Project)

### 小程序常见问题

**Q: 微信开发者工具无法预览**
A: 检查 app.json 配置是否正确

**Q: 预览时报错**
A: 检查页面路径和组件引用

### H5 常见问题

**Q: npm install 失败**
A: 使用淘宝镜像源：`npm config set registry https://registry.npmmirror.com`

**Q: 运行时报错**
A: 检查 node_modules 是否正确安装

---

## 开发环境要求

### iOS 开发环境
- macOS 13.0 或更高版本
- Xcode 15.0 或更高版本
- iOS 15.0 或更高版本（真机/模拟器）

### Android 开发环境
- Windows / macOS / Linux
- Android Studio Hedgehog (2023.1.1) 或更高版本
- Android SDK 24 或更高版本
- JDK 8 或更高版本

### 鸿蒙开发环境
- Windows / macOS
- DevEco Studio 4.0 或更高版本
- HarmonyOS SDK API 9 或更高版本

### 小程序开发环境
- Windows / macOS
- 微信开发者工具 Stable 版本
- 微信账号（用于登录开发者工具）

### H5 开发环境
- Windows / macOS / Linux
- Node.js 18.0 或更高版本
- npm 或 yarn

---

## 技术支持

如有问题，请提交 Issue：
- iOS: https://github.com/xll-gif/ios-login-app/issues
- Android: https://github.com/xll-gif/android-login-app/issues
- 鸿蒙: https://github.com/xll-gif/harmonyos-login-app/issues
- 小程序: https://github.com/xll-gif/miniprogram-login-app/issues
- H5: https://github.com/xll-gif/h5-login-app/issues

---

**创建时间**: 2025-06-20  
**更新时间**: 2025-06-20  
**版本**: v1.0
