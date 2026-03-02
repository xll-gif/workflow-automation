# 需求文档模板

> 使用说明：复制此模板创建新的需求文档，文件名格式为 `REQ-{编号}-{需求名称}.md`

## 基本信息

| 字段 | 内容 |
|-----|------|
| 需求编号 | REQ-001 |
| 需求名称 | [需求名称] |
| 创建日期 | YYYY-MM-DD |
| 负责人 | [负责人姓名] |
| 优先级 | 高 / 中 / 低 |
| 状态 | 待开发 / 开发中 / 已完成 |


## 需求描述

[详细描述需求内容，包括业务背景、目标用户、使用场景等]


## 功能清单

- [ ] 功能点 1
- [ ] 功能点 2
- [ ] 功能点 3


## 设计稿

### MasterGo 设计稿

- **设计稿链接**: [MasterGo 链接](https://mastergo.com/file/xxx)
- **设计稿文件**: `docs/assets/xxx.json`
- **设计图片**: `docs/assets/xxx.png`

### 设计规范

- **主色调**: `#007AFF`
- **辅助色**: `#5AC8FA`
- **背景色**: `#FFFFFF`
- **文字色**: `#333333`


## API 定义

### API 接口

| 接口名称 | 请求方法 | 路径 | 说明 |
|---------|---------|------|------|
| 接口 1 | POST | /api/login | 用户登录 |
| 接口 2 | GET | /api/user/info | 获取用户信息 |

### Postman Collection

- **Collection 链接**: [Postman 链接](https://xxx)
- **Collection 文件**: `docs/api/postman-collection.json`

### Mock 数据

- **Mock 服务**: MSW (Mock Service Worker)
- **Mock 文件**: `src/services/mock.ts`


## 平台实现

### 实现清单

| 平台 | 状态 | 负责人 | 备注 |
|-----|------|--------|------|
| iOS | ⬜ 待开发 | - | - |
| Android | ⬜ 待开发 | - | - |
| 鸿蒙 | ⬜ 待开发 | - | - |
| H5 | ⬜ 待开发 | - | - |
| 小程序 | ⬜ 待开发 | - | - |

### 平台特定需求

#### iOS
- [ ] 最低版本：iOS 15.0+
- [ ] 特定功能：Face ID 登录
- [ ] 其他要求：-

#### Android
- [ ] 最低版本：API 24 (Android 7.0)
- [ ] 特定功能：指纹登录
- [ ] 其他要求：-

#### 鸿蒙
- [ ] 最低版本：API 9 (HarmonyOS 3.0)
- [ ] 特定功能：-
- [ ] 其他要求：-

#### H5
- [ ] 浏览器支持：Chrome 90+, Safari 14+
- [ ] 特定功能：-
- [ ] 其他要求：-

#### 小程序
- [ ] 基础库版本：2.20.0+
- [ ] 特定功能：微信一键登录
- [ ] 其他要求：-


## 组件依赖

### 已有组件

- [ ] Button - 按钮组件
- [ ] InputField - 输入框组件
- [ ] Image - 图片组件
- [ ] Loading - 加载组件

### 需要新建的组件

- [ ] 组件 1 - 描述
- [ ] 组件 2 - 描述


## 验收标准

1. ✅ 功能完整性：所有功能点都已实现
2. ✅ UI 还原度：与设计稿对比，还原度 ≥ 95%
3. ✅ 交互体验：交互流畅，无明显卡顿
4. ✅ 兼容性：各平台测试通过
5. ✅ 代码质量：符合各平台代码规范


## 测试计划

### 单元测试
- [ ] [ ] iOS 单元测试覆盖率 ≥ 80%
- [ ] [ ] Android 单元测试覆盖率 ≥ 80%
- [ ] [ ] H5 单元测试覆盖率 ≥ 80%

### 集成测试
- [ ] API 集成测试通过
- [ ] Mock 数据测试通过

### 端到端测试
- [ ] 登录流程测试通过
- [ ] 异常场景测试通过


## 上线计划

| 阶段 | 时间 | 说明 |
|-----|------|------|
| 开发完成 | YYYY-MM-DD | 代码开发完成 |
| 测试完成 | YYYY-MM-DD | 测试通过 |
| 上线发布 | YYYY-MM-DD | 正式发布 |


## GitHub Issues

### 主 Issue
- **Workflow**: #[1](https://github.com/xll-gif/workflow-automation/issues/1)

### 平台 Issues
- **iOS**: #[1](https://github.com/xll-gif/ios-login-app/issues/1)
- **Android**: #[1](https://github.com/xll-gif/android-login-app/issues/1)
- **鸿蒙**: #[1](https://github.com/xll-gif/harmonyos-login-app/issues/1)
- **H5**: #[1](https://github.com/xll-gif/h5-login-app/issues/1)
- **小程序**: #[1](https://github.com/xll-gif/miniprogram-login-app/issues/1)


## 参考资料

- [需求文档](./)
- [设计规范](./design/)
- [API 文档](./api/)
- [AGENTS.md](../../AGENTS.md)
- [快速开始](./QUICK_START.md)


## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| v1.0 | YYYY-MM-DD | 初始版本 | xxx |
