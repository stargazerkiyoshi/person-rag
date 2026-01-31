## RENAMED Requirements
- FROM: `### Requirement: 关键词检索`
- TO: `### Requirement: 向量检索`

## MODIFIED Requirements
### Requirement: 向量检索
系统 SHALL 使用 PostgreSQL + pgvector 进行向量相似度检索并返回 top-k 片段。
#### Scenario: 命中相似内容
- **WHEN** 查询与资料向量相似度满足检索条件
- **THEN** 返回相关片段

#### Scenario: 无匹配
- **WHEN** 查询未命中任何资料
- **THEN** 返回空结果
