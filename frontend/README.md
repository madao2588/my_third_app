# 前端说明

这是 `Crawler System` 的 Flutter 前端控制台，定位是“爬虫运营与管理后台”，而不是单纯的展示页面。

它主要负责：
- 展示采集结果
- 管理采集任务
- 查看运行状态与日志
- 管理来源站点模板
- 连接后端接口形成完整的运维闭环

## 一、当前已实现的功能

### 1. 仪表盘

用于快速了解系统整体状态：
- 今日新增公告
- 关键词命中公告数
- 监控站点数量
- 高优先级公告数
- 来源站点分布
- 高价值公告列表

### 2. 公告中心

用于查看采集后的业务结果：
- 公告列表
- 公告详情
- 正文查看
- 快照查看
- 关键词命中展示

### 3. 任务管理

这是目前最完整的模块之一，支持：
- 任务列表
- 任务搜索
- 按状态筛选
- 按最近运行结果筛选
- 新建任务
- 编辑任务
- 删除任务
- 启用 / 停用任务
- 立即执行任务
- 自动刷新任务运行状态
- 任务详情
- 最近日志查看
- 从任务反向保存为模板

### 4. 全局日志面板

用于运维排障：
- 日志分页
- 按日志级别筛选
- 按任务 ID 筛选
- 文本搜索
- 日志摘要统计
- 失败任务快捷修复入口
- 从日志直接跳到任务详情 / 编辑 / 重跑

### 5. 来源站点模板管理

这是为了降低任务配置成本而做的模板中心：
- 查看模板目录
- 查看模板标签与说明
- 查看模板建议配置
- 查看模板使用次数和最近使用时间
- 新建模板
- 编辑模板
- 删除模板
- 一键套用模板创建任务

## 二、目录结构

```text
frontend/
|-- docs/                  # 设计与架构文档
|-- lib/
|   |-- app/              # 应用入口、导航和路由壳
|   |-- core/             # 配置、主题、网络层、常量
|   |-- features/         # 业务模块
|   |-- shared/           # 通用模型和组件
|   `-- main.dart
|-- test/
|-- analysis_options.yaml
`-- pubspec.yaml
```

## 三、主要模块说明

### `lib/app`

负责应用级结构：
- 应用入口
- 导航外壳
- 左侧菜单切换
- 跨模块页面组合

### `lib/core`

提供基础设施：
- API 路径常量
- HTTP 客户端
- 主题
- 基础配置

### `lib/features/dashboard`

负责系统首页和概览信息展示。

### `lib/features/notices`

负责公告列表、公告详情、快照查看等。

### `lib/features/system_management`

是当前最重的模块，包含：
- 任务管理
- 日志面板
- 模板相关模型与仓库
- 任务状态追踪

### `lib/features/source_sites`

负责模板目录与模板维护，是“站点蓝图管理页”。

## 四、前端如何与后端协作

前端当前依赖的主要后端接口：

### 仪表盘与公告

- `/v1/dashboard/overview`
- `/v1/notices`
- `/v1/notices/{id}`
- `/v1/notices/{id}/snapshot`

### 任务

- `/v1/tasks`
- `/v1/tasks/{id}`
- `/v1/tasks/{id}/run`

### 日志

- `/v1/logs`
- `/v1/logs/summary`

### 模板

- `/v1/templates/tasks`
- `/v1/templates/tasks/{id}`
- `/v1/templates/tasks/{id}/use`

### 其它（节选）

- `/v1/data/export/csv` — 采集数据 CSV 导出（公告中心等）
- `/v1/keyword-rules` — 关键字规则
- `/v1/auth/login`、`/v1/auth/me` — 登录与会话

## 五、本地运行

```bash
cd frontend   # 或仓库内的 crawler_system/frontend
flutter pub get
flutter run -d chrome
```

**后端地址**：默认 `http://127.0.0.1:8000`，与 `lib/core/config/app_config.dart` 中的 `AppConfig.apiBaseUrl` 一致；若端口或主机不同，请改该常量后重新运行。

**演示登录**：与后端默认管理员一致，账号 **`madao`**、密码 **`666666`**（见登录页底部说明）。

若 Web 端口被占用，可指定端口，例如：

```bash
flutter run -d chrome --web-port=8090
```

静态检查与单元测试：

```bash
flutter analyze
flutter test
```

同仓库下 **后端** 的接口冒烟、登录、登出后会话失效、CSV 导出、**任务创建/读取/删除**，以及日志 / 公告 / 统计 / 看板 / 关键字 / 模板等只读接口与 404 行为单测在 `../server/tests/` 目录，使用 `pytest` 执行；其中 HTTP 用例通过 **会话级共享的 `TestClient`** 只启动一次应用生命周期，避免在 Windows 上多次开关 `TestClient` 时 APScheduler 与事件循环冲突。

前端 `flutter test` 中还包含 **`ApiClient` 与 `http.MockClient`** 的单元测试（成功 JSON、错误 `ApiException`、`postJson` 头与 body），以及对 **`HttpTaskRepository` / `HttpNoticeRepository`** 的 Mock 解析用例，均无需启动真实后端。

## 六、当前前端设计特点

这个前端不是只做页面展示，而是明显偏“运维后台”：
- 交互重点在操作效率
- 信息重点在状态透明
- 页面组织偏控制台式布局
- 模块之间已经开始形成闭环

比如：
- 从模板页可以一键进入任务创建
- 从日志页可以直接跳到任务修复
- 从任务可以反向沉淀模板

## 七、适合继续扩展的方向

如果继续做前端，最值得推进的方向有：

### 1. 模板治理

- 模板目录页已支持**搜索与排序**；可继续做热门模板、保存前校验提示等
- 热门模板
- 模板校验提示

### 2. 任务体验

- 任务分组
- 任务批量操作
- 更详细的运行历史
- 失败原因可视化

### 3. 公告业务能力

- 更多筛选条件
- 标记已读 / 未读
- 收藏与导出
- 业务审阅流程

### 4. 可视化

- 运行趋势图
- 错误趋势图
- 模板使用趋势
- 任务成功率图表

## 八、补充说明

- 当前模板数据已经不再硬编码在页面层，而是通过后端接口获取。
- 模板管理页已经支持 CRUD 和使用统计。
- 前端以 Flutter Web 为优先目标，但结构上也方便后续扩展到桌面端。

如果你接下来要继续维护这个前端，建议优先看：
- `lib/app/navigation/app_shell.dart`
- `lib/features/system_management/`
- `lib/features/source_sites/`
