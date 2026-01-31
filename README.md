# 个人知识库项目

## 本地运行（Node.js + Fastify + TypeScript）
1) 安装依赖
```bash
npm install
```

2) 启动服务
```bash
npm run dev
```
默认监听 `0.0.0.0:8000`，可通过 `PORT` 与 `HOST` 覆盖。

3) 构建与启动
```bash
npm run build
npm start
```

## 配置文件
默认读取 `config/config.json`（参考 `config/config.example.json`），包含账号、JWT、日志、LLM 与数据库配置。  
说明：`config/config.json` 用于本地手动配置（不会提交到仓库）。

### PostgreSQL + pgvector
- 确保 PostgreSQL 已安装并开启 pgvector 扩展：
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
- 配置 `database_url` 指向数据库。

## API 示例
- `GET /health`
- `POST /auth/login`，Body：
```json
{"username":"admin","password":"admin"}
```
- `GET /protected/me`（需 `Authorization: Bearer <token>`）
- `POST /agent`，Body：
```json
{"task":"根据资料整理要点并给出结论","session_id":"可选"}
```

## CLI
```bash
npm run build
node dist/cli.js ingest
node dist/cli.js index
node dist/cli.js query "你的问题"
```

## 前端（Vue + Vite）
1) 安装依赖
```bash
cd frontend
npm install
```

2) 启动开发服务（默认代理到后端 http://127.0.0.1:8000）
```bash
npm run dev
```

3) 自定义后端地址（可选）
```bash
set VITE_API_BASE=http://127.0.0.1:8000
```

4) 构建
```bash
npm run build
```

## 前端配置文件（可选）
可以在 `frontend/public/app-config.json` 中配置运行时参数（参考 `frontend/public/app-config.example.json`）。示例：
```json
{
  "apiBase": "http://127.0.0.1:8000"
}
```
未提供时会回退到 `VITE_API_BASE` 环境变量。

## 本地检索数据
将文本资料放入 `data/` 目录（支持 `.txt`、`.md`），使用 CLI `ingest` 或 `index` 命令写入 pgvector。

## 检索触发策略
智能体会先判断是否需要检索资料：普通对话直接回复；疑似需要资料时才触发检索，并在返回结果中附带来源与执行轨迹。

## 多轮会话
后端会生成 session_id 并在首次响应中返回。前端会自动携带 session_id 进行多轮对话。
