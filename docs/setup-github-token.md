# GitHub Token 配置指南

## 📋 为什么需要 GitHub Token？

GitHub API 需要 Token 进行认证，以便：
- 创建和管理 Issues
- 读写仓库内容
- 提交代码
- 管理 Pull Requests

---

## 🔑 创建 GitHub Personal Access Token

### 步骤 1：访问 Token 创建页面

1. 登录 GitHub：https://github.com
2. 点击右上角头像 → **Settings**（设置）
3. 左侧菜单找到 **Developer settings**（开发者设置）
4. 点击 **Personal access tokens** → **Tokens (classic)**
5. 点击 **Generate new token** → **Generate new token (classic)**

**或者直接访问**：
https://github.com/settings/tokens/new

### 步骤 2：配置 Token

填写以下信息：

| 字段 | 值 |
|-----|---|
| **Note** | `workflow-automation` 或任何描述性名称 |
| **Expiration** | 选择过期时间（建议：No expiration 或 90 days） |

### 步骤 3：设置权限（重要！）

勾选以下权限（最少）：

```
✅ repo                  # 完整仓库访问权限
   - repo:status         # 仓库状态
   - repo_deployment     # 部署
   - public_repo         # 公开仓库
   - repo:invite         # 邀请
   - security_events    # 安全事件

✅ workflow             # 工作流权限
```

**详细权限说明**：

```
✅ repo
  ├─ repo:status        # 提交状态
  ├─ repo_deployment    # 部署状态
  ├─ public_repo        # 公开仓库访问
  ├─ repo:invite        # 邀请协作者
  ├─ security_events    # 安全事件

✅ workflow
  ├─ workflow:run       # 运行工作流
```

**⚠️ 重要提示**：
- 必须勾选 `repo` 权限，否则无法读写仓库
- 如果需要管理 Issues，`repo` 权限是必须的
- 不要勾选不必要的权限，遵循最小权限原则

### 步骤 4：生成并保存 Token

1. 点击页面底部的 **Generate token** 按钮
2. **立即复制 Token**（只会显示一次！）
3. 妥善保存 Token（建议使用密码管理器）

**Token 示例**：
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ⚙️ 配置环境变量

### 方式一：配置到当前 Shell（临时）

```bash
export GITHUB_TOKEN="你的_GITHUB_TOKEN"
```

**验证配置**：
```bash
echo $GITHUB_TOKEN
```

### 方式二：配置到 Shell 配置文件（永久）

#### 对于 Bash：
```bash
echo 'export GITHUB_TOKEN="你的_GITHUB_TOKEN"' >> ~/.bashrc
source ~/.bashrc
```

#### 对于 Zsh：
```bash
echo 'export GITHUB_TOKEN="你的_GITHUB_TOKEN"' >> ~/.zshrc
source ~/.zshrc
```

### 方式三：配置到项目环境文件

在项目根目录创建 `.env` 文件：

```bash
cd /workspace/projects/workflow-automation
echo 'GITHUB_TOKEN="你的_GITHUB_TOKEN"' > .env
```

**⚠️ 重要**：`.env` 文件已添加到 `.gitignore`，不会被提交到 Git

---

## ✅ 验证配置

运行以下命令验证 Token 是否配置成功：

```bash
echo "Checking GitHub Token..."
if [ -z "$GITHUB_TOKEN" ]; then
  echo "❌ GITHUB_TOKEN not set"
else
  echo "✅ GITHUB_TOKEN found (length: ${#GITHUB_TOKEN})"
fi
```

**预期输出**：
```
✅ GITHUB_TOKEN found (length: 40)
```

---

## 🔍 测试 Token 是否有效

使用 curl 测试：

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

**预期响应**：
```json
{
  "login": "xll-gif",
  "id": 123456,
  ...
}
```

---

## 🛡️ 安全建议

### ✅ 最佳实践

1. **不要泄露 Token**：
   - 不要在代码中硬编码 Token
   - 不要提交 Token 到 Git
   - 不要在公开场所分享 Token

2. **使用环境变量**：
   - 将 Token 存储在环境变量中
   - 使用 `.env` 文件管理（已添加到 .gitignore）

3. **定期更新 Token**：
   - 设置合理的过期时间
   - 定期轮换 Token
   - 立即撤销泄露的 Token

4. **限制权限**：
   - 只授予必要的权限
   - 使用最小权限原则
   - 定期审查权限

### ❌ 禁止行为

- ❌ 将 Token 提交到 Git 仓库
- ❌ 在公开代码中硬编码 Token
- ❌ 在公开聊天中分享 Token
- ❌ 使用过期或无效的 Token

---

## 🔄 Token 过期后怎么办？

### 1. 删除旧 Token

1. 访问：https://github.com/settings/tokens
2. 找到旧 Token
3. 点击 **Delete** 删除

### 2. 创建新 Token

按照上述步骤重新创建 Token

### 3. 更新环境变量

```bash
export GITHUB_TOKEN="你的新_GITHUB_TOKEN"
```

---

## 📞 常见问题

### Q1: Token 无效怎么办？

**A**: 检查以下几点：
- Token 是否已过期
- Token 是否被撤销
- Token 是否有正确的权限（`repo`）

### Q2: 为什么需要 `repo` 权限？

**A**: `repo` 权限用于：
- 读写仓库内容
- 创建和管理 Issues
- 提交代码
- 管理 Pull Requests

### Q3: 如何撤销 Token？

**A**:
1. 访问：https://github.com/settings/tokens
2. 找到要撤销的 Token
3. 点击 **Delete** 删除

### Q4: Token 会被提交到 Git 吗？

**A**: 不会！我们已将 `.env` 文件添加到 `.gitignore`，Token 不会被提交。

---

## 📚 相关链接

- [GitHub Personal Access Tokens 官方文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub 权限说明](https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps)
- [GitHub API 文档](https://docs.github.com/en/rest)

---

## ✅ 配置检查清单

- [ ] 已创建 GitHub Personal Access Token
- [ ] 已配置 `repo` 权限
- [ ] 已保存 Token 到安全位置
- [ ] 已配置环境变量 `GITHUB_TOKEN`
- [ ] 已验证 Token 配置成功
- [ ] 已测试 Token 有效性

---

**配置完成后，请告知我，我将帮你自动创建 GitHub Issue！** 🚀
