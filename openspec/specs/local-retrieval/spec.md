# local-retrieval Specification

## Purpose
TBD - created by archiving change add-local-retrieval. Update Purpose after archive.
## Requirements
### Requirement: 本地资料加载
系统 SHALL 从 `data/` 目录加载本地文本资料用于检索。

#### Scenario: 加载本地文本
- **WHEN** `data/` 中存在文本文件
- **THEN** 系统可加载其内容用于检索

### Requirement: 关键词检索
系统 SHALL 使用关键词匹配检索本地资料，并返回 top-k 片段。

#### Scenario: 命中关键词
- **WHEN** 查询关键词命中资料内容
- **THEN** 返回相关片段

#### Scenario: 无匹配
- **WHEN** 查询关键词未命中任何资料
- **THEN** 返回空结果

### Requirement: 智能体检索接入
系统 SHALL 将本地检索结果接入智能体流程。

#### Scenario: 智能体使用检索
- **WHEN** 智能体执行任务
- **THEN** 使用本地检索返回的片段作为上下文

