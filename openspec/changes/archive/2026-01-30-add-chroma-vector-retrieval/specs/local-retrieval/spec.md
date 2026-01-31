## ADDED Requirements
### Requirement: 向量检索
系统 SHALL 支持基于向量的语义检索本地资料，并返回 top-k 片段。

#### Scenario: 语义相近命中
- **WHEN** 查询语义与资料片段相近
- **THEN** 返回相关片段

### Requirement: 向量索引构建
系统 SHALL 提供将本地资料构建为 Chroma 向量索引的方式。

#### Scenario: 构建索引
- **WHEN** 触发索引构建流程
- **THEN** 可将 `data/` 文档写入 Chroma 集合

### Requirement: 检索器切换
系统 SHALL 允许通过配置在关键词检索与向量检索之间切换。

#### Scenario: 启用向量检索
- **WHEN** 配置选择 Chroma 向量检索
- **THEN** 智能体检索使用向量召回结果

## MODIFIED Requirements
### Requirement: 关键词检索
系统 SHALL 支持关键词匹配检索本地资料，并返回 top-k 片段；当配置为关键词检索时使用该策略。

#### Scenario: 命中关键词
- **WHEN** 查询关键词命中资料内容
- **THEN** 返回相关片段

#### Scenario: 无匹配
- **WHEN** 查询关键词未命中任何资料
- **THEN** 返回空结果

#### Scenario: 配置选择关键词检索
- **WHEN** 配置选择关键词检索
- **THEN** 使用关键词匹配检索策略
