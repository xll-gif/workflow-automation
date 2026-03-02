# 需求文档 - 登录页面（完整版）

## 📋 基本信息

| 字段 | 内容 |
|-----|------|
| 需求编号 | REQ-001 |
| 需求名称 | 登录页面 |
| 创建日期 | 2026-03-02 |
| 负责人 | 待定 |
| 优先级 | 🔴 高 |
| 状态 | 🚧 开发中 |
| 需求类型 | 核心功能 |
| 是否需要联调 | ✅ 是 |

---

## 📖 需求描述

### 业务背景
登录页面是用户进入系统的第一道门槛，是应用的核心入口。本需求旨在实现一个跨五端（iOS、Android、鸿蒙、H5、小程序）的统一登录页面，提供安全、流畅的登录体验。

### 目标用户
- 已注册用户
- 需要登录系统的用户
- 新用户（通过注册入口）

### 核心价值
1. 提供统一的登录体验
2. 支持邮箱/密码登录方式
3. 确保登录安全性和用户体验
4. 为后续业务功能提供身份认证基础

---

## 🎯 功能需求

### 核心功能（P0）

#### 1. 登录表单
- [x] 邮箱输入框
  - 支持邮箱格式验证
  - 输入提示文案："请输入邮箱地址"
  - 最大长度：50 个字符
- [x] 密码输入框
  - 支持密码显示/隐藏切换
  - 输入提示文案："请输入密码"
  - 最小长度：6 个字符
  - 最大长度：20 个字符
  - 密码强度提示（弱/中/强）
- [x] 登录按钮
  - 初始状态：禁用（表单未填写完成）
  - 可用状态：可点击
  - 加载状态：显示加载动画
  - 悬停/点击反馈

#### 2. 表单验证
- [x] 实时验证
  - 邮箱格式验证（正则表达式）
  - 密码长度验证（6-20 位）
  - 空值检查
- [x] 提交前验证
  - 所有必填字段验证
  - 防止重复提交（防抖）
- [x] 错误提示
  - 邮箱格式错误："请输入有效的邮箱地址"
  - 密码太短："密码至少需要 6 个字符"
  - 密码太长："密码不能超过 20 个字符"

#### 3. 登录流程
- [x] 用户输入邮箱和密码
- [x] 点击"登录"按钮
- [x] 表单验证（前端）
- [x] 调用登录 API
- [x] 显示加载状态
- [x] 接收 API 响应
  - 成功：跳转到首页
  - 失败：显示错误提示

#### 4. 错误处理
- [x] 网络错误："网络连接失败，请检查网络设置"
- [x] 服务器错误："服务器繁忙，请稍后再试"
- [x] 账号或密码错误："邮箱或密码错误，请重试"
- [x] 账号被锁定："账号已被锁定，请联系客服"

### 辅助功能（P1）

- [ ] 记住密码
  - 开关按钮
  - 本地存储（iOS: Keychain, Android: EncryptedSharedPreferences, H5: localStorage）
  - 默认关闭
- [ ] 找回密码
  - "忘记密码？"链接
  - 跳转到找回密码页面
- [ ] 注册入口
  - "还没有账号？立即注册"链接
  - 跳转到注册页面
- [ ] 第三方登录（可选）
  - 微信登录（小程序专属）
  - Apple ID 登录（iOS 专属）
  - Google 登录（Android 专属）
  - 华为账号登录（鸿蒙专属）

### 增强功能（P2）

- [ ] 自动填充
  - 支持浏览器/系统密码自动填充
  - 支持 OAuth 2.0 授权码自动登录
- [ ] 生物识别登录
  - Face ID 登录（iOS）
  - 指纹登录（Android）
  - 生物识别登录（鸿蒙）
- [ ] 登录历史
  - 记录最近登录时间
  - 显示登录设备信息
- [ ] 安全验证
  - 图形验证码（失败 3 次后）
  - 短信验证码（异地登录）
  - 双因素认证（可选）

---

## 🎨 设计规范

### 设计稿信息

- **设计工具**: MasterGo
- **设计稿链接**: https://mastergo.com/file/185219791981799?fileOpenFrom=home&page_id=M
- **设计文件**: `docs/assets/mastergo_parse_mock.json`
- **设计尺寸**:
  - iOS: 375x667 (iPhone SE) / 390x844 (iPhone 12/13)
  - Android: 360x640 (mdpi) / 360x800 (xdpi)
  - 鸿蒙: 360x640 (mdpi) / 360x800 (xdpi)
  - H5: 1920x1080 (桌面) / 375x667 (移动端)
  - 小程序: 375x667 (iPhone SE)

### 颜色规范

```json
{
  "colors": {
    "primary": "#007AFF",
    "primary_hover": "#0056CC",
    "primary_pressed": "#003D99",
    "secondary": "#5AC8FA",
    "background": "#FFFFFF",
    "background_secondary": "#F5F5F5",
    "text": {
      "primary": "#333333",
      "secondary": "#666666",
      "hint": "#999999",
      "error": "#FF3B30",
      "success": "#34C759"
    },
    "border": {
      "default": "#DDDDDD",
      "focus": "#007AFF",
      "error": "#FF3B30"
    }
  }
}
```

### 字体规范

```json
{
  "fonts": {
    "primary": {
      "family": "PingFang SC, -apple-system, BlinkMacSystemFont, sans-serif",
      "sizes": {
        "h1": 28,
        "h2": 24,
        "h3": 20,
        "body": 16,
        "caption": 14,
        "small": 12
      }
    }
  }
}
```

### 间距规范

```json
{
  "spacing": {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48
  }
}
```

### 圆角规范

```json
{
  "radius": {
    "sm": 4,
    "md": 8,
    "lg": 12,
    "xl": 16,
    "full": 9999
  }
}
```

### 阴影规范

```json
{
  "shadow": {
    "sm": "0 1px 2px rgba(0,0,0,0.05)",
    "md": "0 2px 8px rgba(0,0,0,0.1)",
    "lg": "0 4px 16px rgba(0,0,0,0.15)"
  }
}
```

---

## 🔌 API 定义

### 登录接口

#### 基本信息

| 字段 | 内容 |
|-----|------|
| 接口名称 | 用户登录 |
| 请求方法 | POST |
| 接口路径 | `/api/v1/auth/login` |
| Content-Type | `application/json` |

#### 请求参数

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| email | string | 是 | 用户邮箱 |
| password | string | 是 | 用户密码（6-20 位） |

#### 响应参数

**成功响应 (200)**

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userId": "123456",
    "email": "user@example.com",
    "nickname": "张三",
    "avatar": "https://cdn.example.com/avatar/123456.jpg",
    "expiresIn": 7200
  }
}
```

**失败响应 (400)**

```json
{
  "code": 400,
  "message": "参数错误",
  "errors": [
    {
      "field": "email",
      "message": "邮箱格式不正确"
    }
  ]
}
```

**失败响应 (401)**

```json
{
  "code": 401,
  "message": "邮箱或密码错误"
}
```

**失败响应 (403)**

```json
{
  "code": 403,
  "message": "账号已被锁定，请联系客服",
  "data": {
    "lockReason": "多次登录失败",
    "unlockTime": "2026-02-28T10:00:00Z"
  }
}
```

**失败响应 (500)**

```json
{
  "code": 500,
  "message": "服务器内部错误"
}
```

#### Mock 数据

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "mock_token_1234567890",
    "refreshToken": "mock_refresh_token_0987654321",
    "userId": "MOCK_USER_001",
    "email": "test@example.com",
    "nickname": "测试用户",
    "avatar": "https://via.placeholder.com/100",
    "expiresIn": 7200
  }
}
```

---

## 📐 交互流程

### 正常登录流程

```
用户打开应用
    ↓
显示登录页面
    ↓
用户输入邮箱
    ↓
用户输入密码
    ↓
点击"登录"按钮
    ↓
前端验证表单
    ↓ (验证失败)
显示错误提示
    ↓ (验证成功)
调用登录 API
    ↓ (请求失败)
显示错误提示
    ↓ (请求成功)
保存 Token
    ↓
跳转到首页
```

### 异常流程

#### 1. 邮箱格式错误
```
用户输入错误邮箱 → 实时验证 → 显示"请输入有效的邮箱地址"
```

#### 2. 密码太短
```
用户输入 5 位密码 → 实时验证 → 显示"密码至少需要 6 个字符"
```

#### 3. 网络错误
```
调用 API 失败 → 显示"网络连接失败，请检查网络设置"
```

#### 4. 账号密码错误
```
API 返回 401 → 显示"邮箱或密码错误，请重试"
```

#### 5. 账号被锁定
```
API 返回 403 → 显示"账号已被锁定，请联系客服"
```

---

## 🛡️ 安全要求

### 1. 密码安全
- ✅ 密码在传输前进行加密（建议使用 RSA 加密）
- ✅ 密码不在前端明文存储
- ✅ 密码输入框使用 `secureTextEntry` (iOS) / `inputType="textPassword"` (Android)

### 2. Token 管理
- ✅ Token 存储在安全区域（iOS: Keychain, Android: EncryptedSharedPreferences）
- ✅ Token 有效期为 2 小时
- ✅ Refresh Token 有效期为 7 天
- ✅ Token 过期自动刷新

### 3. 防护措施
- ✅ 防止重复提交（按钮禁用 + 防抖）
- ✅ 登录失败 3 次后显示图形验证码
- ✅ 登录失败 5 次后锁定账号 30 分钟
- ✅ 异地登录提醒

### 4. 数据加密
- ✅ HTTPS 传输
- ✅ Token 使用 JWT 签名
- ✅ 敏感数据不记录日志

---

## 📊 数据埋点

### 埋点事件

| 事件名称 | 触发时机 | 参数 |
|---------|---------|------|
| login_page_view | 登录页面加载完成 | page_source |
| login_input_email | 用户输入邮箱 | input_length |
| login_input_password | 用户输入密码 | input_length |
| login_click | 点击登录按钮 | - |
| login_success | 登录成功 | login_method, duration |
| login_fail | 登录失败 | error_code, error_message |

### 埋点参数说明

```javascript
{
  "page_source": "splash_page | home_page | direct",
  "input_length": 15,
  "login_method": "email | wechat | face_id",
  "duration": 1234,  // 毫秒
  "error_code": "400 | 401 | 403 | 500",
  "error_message": "邮箱或密码错误"
}
```

---

## ♿ 可访问性

### 屏幕阅读器
- ✅ 所有输入框和按钮支持屏幕阅读器
- ✅ 错误提示支持屏幕阅读器

### 键盘导航
- ✅ 支持键盘 Tab 键导航
- ✅ 支持回车键提交表单

### 颜色对比度
- ✅ 文本与背景对比度 ≥ 4.5:1
- ✅ 交互元素与背景对比度 ≥ 3:1

### 字体大小
- ✅ 支持系统字体缩放
- ✅ 最小字体不小于 12px

---

## 📱 平台实现

### iOS (SwiftUI)

**技术栈**
- SwiftUI
- iOS 15.0+

**关键实现**
```swift
- 使用 TextField + SecureField 实现输入框
- 使用 Keychain 存储 Token
- 使用 URLSession 调用 API
- 使用 @State 管理表单状态
```

**平台特定功能**
- Face ID 登录（使用 LocalAuthentication）
- Keychain 存储
- SF Symbols 图标

---

### Android (Kotlin)

**技术栈**
- Jetpack Compose
- API 24+ (Android 7.0)

**关键实现**
```kotlin
- 使用 TextField 实现输入框
- 使用 EncryptedSharedPreferences 存储 Token
- 使用 Retrofit 调用 API
- 使用 StateFlow 管理表单状态
```

**平台特定功能**
- 指纹登录（使用 BiometricPrompt）
- EncryptedSharedPreferences 存储
- Material Design 3

---

### 鸿蒙 (ArkTS)

**技术栈**
- ArkTS
- API 9+ (HarmonyOS 3.0)

**关键实现**
```typescript
- 使用 TextInput 实现输入框
- 使用 preferences 存储 Token
- 使用 @ohos/net/http 调用 API
- 使用 @State 管理表单状态
```

**平台特定功能**
- 生物识别登录
- 华为账号登录
- ArkUI 组件库

---

### H5 (React + TypeScript)

**技术栈**
- React 18
- TypeScript
- Vite
- Axios

**关键实现**
```typescript
- 使用 react-hook-form 管理表单
- 使用 localStorage 存储 Token
- 使用 Axios 调用 API
- 使用 React Router 跳转
```

**平台特定功能**
- 响应式设计
- 浏览器自动填充
- PWA 支持

---

### 小程序 (原生)

**技术栈**
- 微信小程序原生
- 基础库 2.20.0+

**关键实现**
```javascript
- 使用 input 组件实现输入框
- 使用 wx.setStorageSync 存储 Token
- 使用 wx.request 调用 API
- 使用 wx.navigateTo 跳转
```

**平台特定功能**
- 微信一键登录
- 手机号快速验证
- 自定义导航栏

---

## ✅ 验收标准

### 功能验收

| 验收项 | 标准 | 验证方式 |
|-------|------|---------|
| 登录功能 | 输入正确邮箱密码后成功登录 | 手动测试 |
| 表单验证 | 错误输入实时提示 | 手动测试 |
| 错误处理 | 网络错误、API 错误正确提示 | 手动测试 |
| Token 存储 | Token 安全存储，刷新有效 | 代码审查 |
| 跳转功能 | 登录成功后跳转到首页 | 手动测试 |

### UI 验收

| 验收项 | 标准 | 验证方式 |
|-------|------|---------|
| 还原度 | 与设计稿对比 ≥ 95% | 视觉对比 |
| 响应式 | 适配各平台主流机型 | 真机测试 |
| 动画 | 交互动画流畅（≥ 60fps） | 性能测试 |
| 字体 | 字体大小、颜色符合规范 | 视觉对比 |

### 性能验收

| 验收项 | 标准 | 验证方式 |
|-------|------|---------|
| 页面加载 | 首屏加载 ≤ 2s | 性能测试 |
| API 响应 | 登录请求 ≤ 1s | 接口测试 |
| 内存占用 | 内存占用 ≤ 100MB | 性能测试 |

### 安全验收

| 验收项 | 标准 | 验证方式 |
|-------|------|---------|
| 密码传输 | 密码加密传输 | 网络抓包 |
| Token 存储 | Token 安全存储 | 代码审查 |
| 防重放 | 防止重复提交 | 手动测试 |

---

## 🧪 测试计划

### 单元测试

| 平台 | 覆盖率要求 | 测试框架 |
|-----|-----------|---------|
| iOS | ≥ 80% | XCTest |
| Android | ≥ 80% | JUnit |
| 鸿蒙 | ≥ 80% | ArkTS Test |
| H5 | ≥ 80% | Jest + React Testing Library |
| 小程序 | ≥ 60% | Jest |

### 集成测试

- [ ] API 集成测试（使用 Mock 数据）
- [ ] 组件集成测试
- [ ] 路由集成测试

### 端到端测试

| 场景 | 预期结果 | 测试方式 |
|-----|---------|---------|
| 正常登录 | 跳转到首页 | 手动测试 |
| 邮箱格式错误 | 显示错误提示 | 手动测试 |
| 密码错误 | 显示错误提示 | 手动测试 |
| 网络错误 | 显示网络错误提示 | 手动测试 |
| 账号锁定 | 显示锁定提示 | 手动测试 |

### 兼容性测试

| 平台 | 测试机型/浏览器 |
|-----|---------------|
| iOS | iPhone SE, iPhone 12, iPhone 14 |
| Android | 小米 13, 华为 P50, OPPO Find X5 |
| 鸿蒙 | 华为 Mate 50, 华为 P60 |
| H5 | Chrome, Safari, Firefox, Edge |
| 小程序 | 微信 8.0+ |

---

## 📅 上线计划

| 阶段 | 时间 | 里程碑 | 负责人 |
|-----|------|-------|--------|
| 需求评审 | 2026-02-27 | 需求文档确认 | 待定 |
| 设计交付 | 2026-02-28 | 设计稿交付 | 设计师 |
| 开发完成 | 2026-03-04 | 代码开发完成 | 开发 |
| 自测完成 | 2026-03-04 | 单元测试通过 | 开发 |
| 集成测试 | 2026-03-05 | 集成测试通过 | 测试 |
| UAT 测试 | 2026-03-05 | 用户验收通过 | 产品 |
| 上线发布 | 2026-03-06 | 正式发布上线 | 运维 |

---

## 🔗 相关链接

### 文档链接
- [需求文档模板](./REQUIREMENT_TEMPLATE.md)
- [设计规范文档](../design/design-system.md)
- [API 文档](../api/authentication.md)

### 代码仓库
- **Workflow**: [workflow-automation](https://github.com/xll-gif/workflow-automation)
- **iOS**: [ios-login-app](https://github.com/xll-gif/ios-login-app)
- **Android**: [android-login-app](https://github.com/xll-gif/android-login-app)
- **鸿蒙**: [harmonyos-login-app](https://github.com/xll-gif/harmonyos-login-app)
- **H5**: [h5-login-app](https://github.com/xll-gif/h5-login-app)
- **小程序**: [miniprogram-login-app](https://github.com/xll-gif/miniprogram-login-app)

### GitHub Issues
- **主 Issue**: [#1 [REQ-001] 登录页面](https://github.com/xll-gif/workflow-automation/issues/1) ✅
- iOS Issue: [待创建](https://github.com/xll-gif/ios-login-app/issues/1)
- Android Issue: [待创建](https://github.com/xll-gif/android-login-app/issues/1)
- 鸿蒙 Issue: [待创建](https://github.com/xll-gif/harmonyos-login-app/issues/1)
- H5 Issue: [待创建](https://github.com/xll-gif/h5-login-app/issues/1)
- 小程序 Issue: [待创建](https://github.com/xll-gif/miniprogram-login-app/issues/1)

---

## 📝 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|-------|
| v1.1 | 2026-03-02 | 创建 GitHub Issue #1，更新需求文档链接 | xll-gif |
| v1.0 | 2026-02-27 | 初始版本创建 | - |

---

## 📞 联系方式

| 角色 | 姓名 | 邮箱 |
|-----|------|------|
| 产品经理 | 待定 | - |
| 设计师 | 待定 | - |
| 开发负责人 | 待定 | - |
| 测试负责人 | 待定 | - |

---

**文档版本**: v1.1
**最后更新**: 2026-03-02
