## MODIFIED Requirements
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

#### Scenario: 未触发检索
- **WHEN** 模型判断无需检索即可回答
- **THEN** 系统跳过检索并返回纯对话结果

#### Scenario: 触发检索
- **WHEN** 模型判断需要资料支撑
- **THEN** 系统执行检索并返回来源与轨迹