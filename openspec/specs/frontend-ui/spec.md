# frontend-ui Specification

## Purpose
TBD - created by archiving change add-frontend-ui. Update Purpose after archive.
## Requirements
### Requirement: 前端应用骨架
系统 SHALL 提供位于 `frontend/` 的 Vue 3 前端应用，并基于 Vite、Tailwind CSS 与 Less 构建。

#### Scenario: 启动开发服务
- **WHEN** 用户运行前端开发命令
- **THEN** 界面在本地可访问并能连接后端 API

### Requirement: 登录流程
系统 SHALL 允许用户向 `/auth/login` 提交凭证，并保存返回的访问令牌用于后续请求。

#### Scenario: 用户成功登录
- **WHEN** 用户在登录页提交有效凭证
- **THEN** 前端保存访问令牌以调用受保护接口

### Requirement: 受保护的个人信息页
系统 SHALL 使用保存的令牌调用 `/protected/me` 并展示当前用户信息。

#### Scenario: 登录后查看个人信息
- **WHEN** 用户已完成认证
- **THEN** 前端拉取个人信息并展示用户名

