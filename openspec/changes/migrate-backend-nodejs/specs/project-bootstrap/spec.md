## MODIFIED Requirements
### Requirement: 依赖管理
系统 SHALL 使用 `package.json` 管理 Node.js 依赖并锁定版本。
#### Scenario: 安装依赖
- **WHEN** 开发者运行 `npm install`
- **THEN** 依赖可以无交互安装

### Requirement: 基础 API 服务
系统 SHALL 提供 Fastify 应用与健康检查接口。
#### Scenario: 健康检查
- **WHEN** 客户端发送 `GET /health`
- **THEN** API 返回 200 且包含状态信息

## ADDED Requirements
### Requirement: TypeScript 运行与编译
系统 SHALL 使用 TypeScript 作为后端主要实现语言，并提供可执行构建产物。
#### Scenario: 构建产物可用
- **WHEN** 开发者运行构建脚本
- **THEN** 生成可在 Node.js 下运行的产物
