## ADDED Requirements

### Requirement: 项目结构
系统 SHALL 提供标准项目目录结构，用于源代码、测试、配置与脚本。

#### Scenario: 仓库结构存在
- **WHEN** 开发者打开仓库
- **THEN** 存在 `src/`、`tests/`、`config/`、`scripts/` 目录

### Requirement: 依赖管理
系统 SHALL 使用 `requirements.txt` 定义依赖并锁定版本。

#### Scenario: 安装依赖
- **WHEN** 开发者运行 `pip install -r requirements.txt`
- **THEN** 依赖可以无交互安装

### Requirement: 基础 API 服务
系统 SHALL 提供 FastAPI 应用与健康检查接口。

#### Scenario: 健康检查
- **WHEN** 客户端发送 `GET /health`
- **THEN** API 返回 200 且包含状态信息

### Requirement: 配置加载
系统 SHALL 从环境变量与可选配置文件加载配置。

#### Scenario: 环境变量覆盖
- **WHEN** 为某配置项设置环境变量
- **THEN** 环境变量值覆盖配置文件

### Requirement: 日志初始化
系统 SHALL 初始化应用日志并支持可配置日志级别。

#### Scenario: Debug 日志
- **WHEN** 配置 `LOG_LEVEL=DEBUG`
- **THEN** 输出 debug 级别日志

### Requirement: CLI 框架
系统 SHALL 提供 CLI 入口，包含 `ingest`、`index`、`query` 子命令。

#### Scenario: CLI 帮助信息
- **WHEN** 开发者运行 CLI 的 `--help`
- **THEN** 显示可用子命令列表
