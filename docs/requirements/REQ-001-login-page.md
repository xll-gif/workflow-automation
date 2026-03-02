# 需求文档 - 登录页面

## 基本信息

| 字段 | 内容 |
|-----|------|
| 需求编号 | REQ-001 |
| 需求名称 | 登录页面 |
| 创建日期 | 2026-02-27 |
| 负责人 | 待定 |
| 优先级 | 高 |
| 状态 | 开发中 |


## 需求描述

### 业务背景
用户需要通过登录页面进入应用系统，支持邮箱/密码登录方式，为后续业务功能提供身份认证基础。

### 目标用户
- 已注册用户
- 需要登录系统的用户

### 使用场景
1. 用户打开应用，进入登录页面
2. 用户输入邮箱和密码
3. 系统验证用户信息
4. 验证成功后进入首页


## 功能清单

- [x] 登录页面 UI 开发
- [x] 邮箱输入框
- [x] 密码输入框
- [x] 登录按钮
- [x] 表单验证
- [x] 错误提示
- [x] Mock 数据联调
- [ ] API 集成
- [ ] 加载状态
- [ ] 记住密码
- [ ] 找回密码
- [ ] 注册入口


## 设计稿

### MasterGo 设计稿

- **设计稿链接**: https://mastergo.com/file/185219791981799?fileOpenFrom=home&page_id=M
- **设计稿文件**: `docs/assets/mastergo_parse_mock.json`
- **设计规范**: 参考 `docs/assets/mastergo_parse_mock.json`

### 设计规范

```json
{
  "colors": {
    "primary": "#007AFF",
    "secondary": "#5AC8FA",
    "background": "#FFFFFF",
    "text": "#333333",
    "border": "#DDDDDD"
  }
}
```


## API 定义

### API 接口

| 接口名称 | 请求方法 | 路径 | 说明 |
|---------|---------|------|------|
| 用户登录 | POST | /api/v1/auth/login | 用户登录 |

### 请求参数

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### 响应参数

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userId": "123456",
    "email": "user@example.com"
  }
}
```

### Mock 数据

- **Mock 服务**: MSW (Mock Service Worker)
- **Mock 文件**: 参考各平台的 mock 服务实现


## 平台实现

### 实现清单

| 平台 | 状态 | 负责人 | 备注 |
|-----|------|--------|------|
| iOS | ⬜ 待开发 | - | - |
| Android | ⬜ 待开发 | - | - |
| 鸿蒙 | ⬜ 待开发 | - | - |
| H5 | ✅ 已开发 | - | 已生成基础代码 |
| 小程序 | ⬜ 待开发 | - | - |

### 平台特定需求

#### iOS
- [ ] 最低版本：iOS 15.0+
- [ ] 特定功能：Face ID 登录（可选）
- [ ] 其他要求：-

#### Android
- [ ] 最低版本：API 24 (Android 7.0)
- [ ] 特定功能：指纹登录（可选）
- [ ] 其他要求：-

#### 鸿蒙
- [ ] 最低版本：API 9 (HarmonyOS 3.0)
- [ ] 特定功能：-
- [ ] 其他要求：-

#### H5
- [ ] 浏览器支持：Chrome 90+, Safari 14+
- [ ] 特定功能：-
- [ ] 其他要求：已完成基础组件和页面

#### 小程序
- [ ] 基础库版本：2.20.0+
- [ ] 特定功能：微信一键登录
- [ ] 其他要求：-


## 组件依赖

### 已有组件 ✅

- [x] Button - 按钮组件（已实现）
- [x] InputField - 输入框组件（已实现）
- [ ] Image - 图片组件（待实现）
- [ ] Loading - 加载组件（待实现）

### 需要新建的组件

- [ ] Logo - Logo 组件
- [ ] Form - 表单组件
- [ ] Link - 链接组件


## 验收标准

1. ✅ 功能完整性：邮箱输入、密码输入、登录按钮、表单验证、错误提示
2. ✅ UI 还原度：与设计稿对比，还原度 ≥ 95%
3. ✅ 交互体验：输入流畅，按钮响应及时
4. ✅ 兼容性：各平台测试通过
5. ✅ 代码质量：符合各平台代码规范


## 测试计划

### 单元测试
- [ ] iOS 单元测试覆盖率 ≥ 80%
- [ ] Android 单元测试覆盖率 ≥ 80%
- [ ] H5 单元测试覆盖率 ≥ 80%

### 集成测试
- [ ] API 集成测试通过
- [ ] Mock 数据测试通过

### 端到端测试
- [ ] 登录流程测试通过
- [ ] 异常场景测试通过（错误邮箱、错误密码）


## 上线计划

| 阶段 | 时间 | 说明 |
|-----|------|------|
| 开发完成 | 2026-03-05 | 代码开发完成 |
| 测试完成 | 2026-03-06 | 测试通过 |
| 上线发布 | 2026-03-07 | 正式发布 |


## GitHub Issues

### 主 Issue
- **Workflow**: [待创建](https://github.com/xll-gif/workflow-automation/issues)

### 平台 Issues
- **iOS**: [待创建](https://github.com/xll-gif/ios-login-app/issues)
- **Android**: [待创建](https://github.com/xll-gif/android-login-app/issues)
- **鸿蒙**: [待创建](https://github.com/xll-gif/harmonyos-login-app/issues)
- **H5**: [待创建](https://github.com/xll-gif/h5-login-app/issues)
- **小程序**: [待创建](https://github.com/xll-gif/miniprogram-login-app/issues)


## 参考资料

- [需求文档模板](./REQUIREMENT_TEMPLATE.md)
- [设计稿解析](../assets/mastergo_parse_mock.json)
- [API 文档](../api/)
- [AGENTS.md](../../AGENTS.md)
- [快速开始](../QUICK_START.md)


## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| v1.0 | 2026-02-27 | 初始版本 | workflow-automation |
