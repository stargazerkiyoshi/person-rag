## MODIFIED Requirements
### Requirement: 会话上下文记录
系统 SHALL 使用 PostgreSQL 持久化会话历史，并在生成回复时仅使用最近 N 轮对话。
#### Scenario: 使用最近对话
- **WHEN** 会话中存在多轮历史
- **THEN** 系统仅使用最近 N 轮作为上下文
