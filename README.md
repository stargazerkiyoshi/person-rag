# 个人知识库项目

## 本地运行
1) 安装依赖
```bash
pip install -r requirements.txt
```

2) 配置环境变量（示例）
```bash
set APP_USERNAME=admin
set APP_PASSWORD=admin
set JWT_SECRET=change-me
set JWT_EXPIRE_MINUTES=60
set LOG_LEVEL=INFO
```

3) 启动服务
```bash
python -m src.main
```

## 配置文件
可选配置文件：`config/config.json`（参考 `config/config.example.json`）。
如需使用配置文件，请设置：
```bash
set CONFIG_FILE=config/config.json
```

## API 示例
- `GET /health`
- `POST /auth/login`，Body：
```json
{"username":"admin","password":"admin"}
```
- `GET /protected/me`（需 `Authorization: Bearer <token>`）


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
