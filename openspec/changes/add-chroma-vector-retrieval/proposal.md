# 变更：新增基于 Chroma 的向量检索

## 为什么
现有检索仅支持关键词匹配，难以覆盖语义相近的查询；需要引入向量检索提升召回质量。

## 变更内容
- 新增 Chroma 向量检索实现，使用本地 embedding（中英双语、质量优先）
- 新增向量索引构建流程与必要配置项
- 检索器按配置可在关键词检索与向量检索间切换

## 影响范围
- 受影响规格：local-retrieval
- 受影响代码：src/agent/retriever.py, src/agent/runner.py, src/core/config.py, scripts/build_chroma_index.py, requirements.txt, config/config.json
