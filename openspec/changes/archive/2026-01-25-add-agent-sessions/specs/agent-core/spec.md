## ADDED Requirements
### Requirement: 会话标识返回
系统 SHALL 在首次请求未提供 session_id 时生成并在响应中返回 session_id。

#### Scenario: 会话标识返回
- **WHEN** 客户端首次请求未提供 session_id
- **THEN** 系统生成 session_id 并在响应中返回

### Requirement: 会话上下文记忆
系统 SHALL 使用 SQLite 持久化会话历史，并在生成回复时仅使用最近 N 轮对话。

#### Scenario: 使用最近对话
- **WHEN** 会话中存在多轮历史
- **THEN** 系统仅使用最近 N 轮作为上下文