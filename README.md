# 个人知识库项目

## 本地运行
1) 安装依赖
```bash
pip install -r requirements.txt
```

2) 启动服务
```bash
python -m src.main
```

## 配置文件
默认读取 `config/config.json`（参考 `config/config.example.json`），包含账号、JWT、日志与大模型相关配置。  
说明：`config/config.json` 用于本地手动配置（不会提交到仓库）。

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

## 前端智能体对话
启动前端后，登录进入界面，点击“智能体对话”进入多轮对话页面。

## 本地检索数据
将文本资料放入 `data/` 目录（支持 `.txt`、`.md`），智能体会进行关键词检索并在命中时作为上下文使用。

## 检索触发策略
智能体会先判断是否需要检索资料：普通对话直接回复；疑似需要资料时才触发检索，并在返回结果中附带来源与执行轨迹。

## 多轮会话
后端会生成 session_id 并在首次响应中返回。前端会自动携带 session_id 进行多轮对话。
