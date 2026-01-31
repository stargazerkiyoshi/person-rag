# 变更：后端迁移到 Node.js + Fastify + TypeScript

## 为什么
当前后端基于 Python/FastAPI。为统一技术栈、提升运行时一致性与可维护性，计划将后端全面迁移到 Node.js，并采用 Fastify + TypeScript。

## 变更内容
- **破坏性变更**：后端运行时从 Python/FastAPI 迁移为 Node.js/Fastify + TypeScript
- **破坏性变更**：依赖管理由 `requirements.txt` 迁移为 `package.json`
- 使用 PostgreSQL + pgvector 作为向量存储与检索后端
- 全面迁移 API、索引、检索、解析与模型调用实现
- 不保留 Python 代码与实现

## 影响范围
- 受影响规格：project-bootstrap、agent-core、local-retrieval
- 受影响代码：`src/`、`config/`、`scripts/`、`tests/`、`frontend/`（API 交互保持一致但实现迁移）
- 相关变更：现有 `add-chroma-vector-retrieval` 可能与新的向量方案冲突，需要协调
