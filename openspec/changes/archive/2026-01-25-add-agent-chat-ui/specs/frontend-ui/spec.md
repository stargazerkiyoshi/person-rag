## ADDED Requirements
### Requirement: 智能体对话页面
系统 SHALL 提供智能体对话页面，用于提交任务并显示返回的回答。

#### Scenario: 提交任务
- **WHEN** 用户输入任务并点击发送
- **THEN** 前端调用 POST /agent 并展示返回回答

### Requirement: 多轮对话展示
系统 SHALL 支持多轮对话记录，按时间顺序展示用户输入与智能体回答。

#### Scenario: 连续对话
- **WHEN** 用户连续提交多轮任务
- **THEN** 界面显示完整的对话历史

### Requirement: 结果详情展示
系统 SHALL 展示来源列表、执行轨迹与动作结果信息。

#### Scenario: 展示详情
- **WHEN** 智能体返回来源与轨迹信息
- **THEN** 界面展示来源、轨迹步骤与动作结果

### Requirement: 前端组件库
系统 SHALL 使用 Arco Design 组件库渲染关键交互组件（如按钮、输入、卡片与提示）。

#### Scenario: 使用组件库
- **WHEN** 用户访问登录、个人信息与智能体对话页面
- **THEN** 页面使用 Arco Design 组件完成主要交互与展示

### Requirement: 前端运行时配置
系统 SHALL 支持通过前端配置文件与环境变量设置后端 API 地址。

#### Scenario: 使用配置文件
- **WHEN** 提供 `frontend/public/app-config.json`
- **THEN** 前端优先读取文件中的 `apiBase` 配置

#### Scenario: 使用环境变量
- **WHEN** 未提供配置文件且设置 `VITE_API_BASE`
- **THEN** 前端使用环境变量中的后端地址

### Requirement: 前端网络请求
系统 SHALL 使用 Axios 作为前端 HTTP 请求库调用后端接口。

#### Scenario: 发送智能体请求
- **WHEN** 前端发起 POST /agent 请求
- **THEN** 使用 Axios 发送请求并处理返回
