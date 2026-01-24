## 1. 实施
- [x] 1.1 创建项目目录结构（`src/`、`tests/`、`config/`、`scripts/`）
- [x] 1.2 添加 `requirements.txt` 并锁定依赖版本
- [x] 1.3 搭建 FastAPI 应用骨架与 `GET /health` 接口
- [x] 1.4 添加配置加载（环境变量 + 可选配置文件）
- [x] 1.5 添加日志初始化与可配置等级
- [x] 1.6 添加 CLI 框架（`ingest`、`index`、`query` 占位）
- [x] 1.7 添加单用户登录配置（用户名 + 密码/密钥）
- [x] 1.8 添加登录接口并签发 JWT
- [x] 1.9 添加 JWT 鉴权中间件与受保护接口
- [x] 1.10 添加健康检查与登录相关测试
- [x] 1.11 添加本地运行与环境变量说明文档

## 2. 验证
- [ ] 2.1 运行单元测试
- [x] 2.2 运行 `openspec validate add-project-bootstrap-auth --strict --no-interactive`
