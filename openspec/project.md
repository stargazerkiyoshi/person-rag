# Project Context / 项目上下文

## Purpose / 项目目标
打造一个个人知识库，用于存储我搜集到的资料，并在需要时通过提问获得基于资料的回答；同时支持对资料进行深入研究与分析。

成功标准（初期）：
- 能导入本地文档与互联网资料
- 能基于资料回答问题并支持多种分析方式
- 可在本地稳定运行

## Tech Stack / 技术栈
- 语言与框架：Python 3.11 + FastAPI
- LLM 接入：火山云模型 + 本地模型（Ollama）双通道，接口抽象化
- 向量数据库：本地 FAISS 起步，后续可切换火山云向量检索服务
- Embedding：优先火山云 Embedding，本地备选 bge-small
- 文档解析：pdfplumber（PDF）、python-docx（DOC）、Markdown 解析器、网页解析（Readability/BeautifulSoup）
- 元数据存储：SQLite
- 依赖管理：requirements.txt

## Project Conventions / 项目规范

### Code Style / 代码风格
- Python 格式化与规范：black + ruff（必要时加 isort）
- 命名约定：函数与变量 snake_case，类名 PascalCase

### Architecture Patterns / 架构模式
- 模块分层：Ingest → Index → Retrieve → Answer
- LLM 与向量库采用适配层，确保可替换
- 文档抽取与清洗统一输出为标准化文本块

### Testing Strategy / 测试策略
- 单元测试：解析、切分、检索逻辑
- 回归样例：固定问题输出包含关键词
- 少量端到端：导入→索引→检索→回答

### Git Workflow / Git 工作流
- master 为稳定分支
- 功能分支命名：feat/xxx，修复分支：fix/xxx
- 提交信息：feat: / fix: / chore:

## Domain Context / 领域背景
- 场景 1：复习和研究计算机知识，回顾知识点并进行思考与扩展研究
- 场景 2：游戏攻略研究，查询人物技能与装备信息并进行策略分析
- 资料来源包括互联网与本地文档
- 输入形式包括 PDF / Markdown / DOC / 网页
- 用户以“问题”为主要交互入口

## Important Constraints / 重要约束
- 隐私要求：必须保证私人资料不可被他人访问
- 权限模型：账号权限控制
- 初期为单用户模式
- 性能要求：初期不高，功能优先
- 规模预期：初期数据量较小，未来可能增长

## External Dependencies / 外部依赖
- 火山云大模型与 Embedding 服务（可选）
- 火山云向量检索服务（可选）
- 本地模型运行（Ollama）

## Additional Project Context / 补充项目背景

### Scope and Non-Goals / 范围与非目标
范围（MVP）：
- 资料导入（本地文档 + 互联网资料）
- 问答与基于资料的分析
- 基础的整理与检索能力

非目标（当前不做）：
- 面向多人协作或公开分享
- 大规模性能优化与自动化运维
- 深度个性化推荐系统

### Knowledge Organization Strategy / 知识组织策略
- 允许原始资料与整理后的知识条目并存
- 支持主题/标签的轻量组织方式
- 结构化程度以“可检索和可分析”为目标

### Retrieval and Answering / 检索与问答
- 以问题驱动的问答为主
- 回答必须基于资料来源
- 分析方式包括：对比、总结、推理、结构化输出
- 分析方式由提示词决定，优先级同等

### RAG / Model Strategy / RAG 与模型策略
- 初期可先简化实现，保证“能回答”
- 采用本地与云端双通道模型，按成本与场景切换
- 预留向量库迁移能力，支持本地到火山云平滑切换

### Roadmap / 版本规划
- MVP：资料导入 + 问答 + 基础整理
- 下一阶段：更好的分析模式与多种回答风格
- 未来阶段：自动化收集兴趣主题并整理归纳

### Auto-Collection Policy / 自动收集策略
- 触发方式：用户输入感兴趣主题与 URL
- 以手动触发为主
- 频率不会太高

### OpenSpec Workflow / OpenSpec 工作流
- 所有新能力或较大变更使用 OpenSpec 变更流程
- 需求以明确场景与可验证条件描述
