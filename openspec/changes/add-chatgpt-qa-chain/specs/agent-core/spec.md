## ADDED Requirements
### Requirement: 可插拔模型提供方配置
系统 SHALL 从环境变量或配置文件加载可插拔模型提供方配置，包括提供方标识、API 密钥和模型名，并支持可选的基础地址与超时设置。

#### Scenario: 缺少 API 密钥
- **WHEN** 发起智能体请求时未配置 API 密钥
- **THEN** 系统返回明确的配置错误且不调用 ChatGPT

#### Scenario: 自定义基础地址
- **WHEN** 配置了基础地址
- **THEN** 请求使用该基础地址

#### Scenario: 切换提供方
- **WHEN** 配置提供方标识为其他可用提供方
- **THEN** 系统按所选提供方创建模型调用

### Requirement: 智能体接口
系统 SHALL 提供 POST /agent 接口，接收任务并返回结果与执行轨迹。

#### Scenario: 智能体任务请求
- **WHEN** 客户端发送合法任务
- **THEN** 响应包含结果与执行轨迹

### Requirement: 智能体流程编排
系统 SHALL 执行检索、整理、多步分析与动作执行，并在最终结果中说明使用到的来源。

#### Scenario: 命中相关上下文
- **WHEN** 检索返回一个或多个片段
- **THEN** 结果引用使用到的来源

#### Scenario: 未命中上下文
- **WHEN** 检索未返回片段
- **THEN** 结果说明信息不足并返回空来源列表

#### Scenario: 动作执行失败
- **WHEN** 动作执行失败
- **THEN** 结果说明失败原因并记录到执行轨迹
