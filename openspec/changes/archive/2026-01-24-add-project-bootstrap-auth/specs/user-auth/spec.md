## ADDED Requirements

### Requirement: 单用户账号
系统 SHALL 支持通过环境变量或配置文件设置的单用户账号，并 SHALL 不提供自注册功能。

#### Scenario: 使用配置账号登录
- **WHEN** 用户提交已配置的用户名与密码
- **THEN** 系统接受登录请求

#### Scenario: 注册不可用
- **WHEN** 用户尝试访问注册接口
- **THEN** API 返回 404

### Requirement: JWT 登录
系统 SHALL 在登录成功后签发 JWT 访问令牌。

#### Scenario: 登录返回令牌
- **WHEN** 提供有效凭证
- **THEN** 响应包含访问令牌与过期信息

### Requirement: 受保护接口
系统 SHALL 要求访问受保护 API 时提供有效 JWT。

#### Scenario: 缺少令牌
- **WHEN** 请求未携带令牌
- **THEN** API 返回 401

#### Scenario: 令牌有效
- **WHEN** 请求携带有效令牌
- **THEN** API 返回受保护资源

### Requirement: 令牌过期
系统 SHALL 支持配置 JWT 过期时长。

#### Scenario: 配置过期时长
- **WHEN** 过期时长设置为 10 分钟
- **THEN** 签发的令牌包含 10 分钟过期时间
