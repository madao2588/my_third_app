# Crawler System 爬虫运营平台

这是一个基于 FastAPI 和 Flutter 构建的爬虫运营平台，目标不是只做“抓取脚本”，而是提供一套可管理、可观察、可复用的采集系统。

当前项目已经具备以下能力：

- 任务管理：创建、编辑、启用、停用、删除、立即执行
- 任务状态跟踪：`queued`、`running`、`success`、`failed`
- 采集链路：下载、解析、清洗、质量评分、去重、入库、快照保存
- 日志体系：全局日志、任务日志、日志摘要统计
- 模板体系：模板列表、模板创建/编辑/删除、模板一键套用、模板使用次数统计
- Flutter 运维控制台：仪表盘、公告中心、任务管理、全局日志、来源站点模板管理

## 一、项目定位

这个项目适合用于以下场景：

- 招标公告、通知公告、新闻资讯等网页信息采集
- 需要定时抓取并保留快照的业务系统
- 需要多人协作维护采集规则、模板和任务的内部平台
- 想把“爬虫脚本”升级成“可运营的采集系统”

相比临时脚本，本项目更强调：

- 可维护：任务、模板、日志都有明确结构
- 可追踪：每次运行的状态和错误可以回看
- 可复用：站点模板可以沉淀和复用
- 可扩展：后续可以继续接入多页抓取、模板治理、导出能力等

## 二、技术栈

### 后端

- Python 3.11+（建议使用 3.11；当前也已在 3.14 环境验证）
- FastAPI
- SQLAlchemy Async
- SQLite
- APScheduler
- httpx
- Playwright
- readability-lxml
- BeautifulSoup / lxml

### 前端

- Flutter
- Flutter Web 优先
- Material 3

## 三、目录结构

```text
crawler_system/
|-- server/
|   |-- app/
|   |   |-- api/              # API 路由
|   |   |-- core/             # 配置、数据库、生命周期、调度器
|   |   |-- engine/           # 抓取、解析、清洗、校验流水线
|   |   |-- models/           # 数据模型
|   |   |-- repositories/     # 数据访问层
|   |   |-- schemas/          # 请求/响应模型
|   |   `-- services/         # 业务服务层
|   |-- storage/
|   |   |-- snapshots/        # 页面快照
|   |   |-- exports/          # 导出目录
|   |   `-- templates/        # 模板文件存储
|   |-- data.db
|   |-- main.py
|   `-- requirements.txt
|-- frontend/
|   |-- docs/
|   |-- lib/
|   |-- test/
|   `-- pubspec.yaml
|-- docker-compose.yml
`-- README.md
```

## 四、后端能力说明

### 1. 任务管理

任务是整个系统的核心对象，包含：

- 任务名称
- 起始 URL
- 解析规则
- Cron 表达式
- 启用状态
- 最近运行状态
- 最近成功时间
- 最近错误信息

当前接口：

- `GET /v1/tasks`
- `GET /v1/tasks/{id}`
- `POST /v1/tasks`
- `PUT /v1/tasks/{id}`
- `DELETE /v1/tasks/{id}`
- `POST /v1/tasks/{id}/run`

### 2. 采集数据

系统会对采集内容进行处理并保存：

- 原始 HTML 内容
- 清洗后的正文文本
- 标题
- 来源 URL
- 质量评分
- 内容哈希
- 抓取时间
- 快照路径

相关接口：

- `GET /v1/data`
- `GET /v1/data/{id}`
- `GET /v1/data/{id}/snapshot`

### 3. 公告与仪表盘

在采集数据基础上，系统还提供了更贴近业务的“公告视图”和“仪表盘统计”：

- 公告列表和详情
- 关键词命中
- 高优先级判断
- 来源站点分布
- 近期公告概览

相关接口：

- `GET /v1/notices`
- `GET /v1/notices/{id}`
- `GET /v1/notices/{id}/snapshot`
- `GET /v1/dashboard/overview`

### 4. 日志系统

系统会记录：

- 任务执行完成
- 任务执行失败
- 静态抓取失败后回退动态抓取
- 解析规则异常
- 快照保存失败
- 全局异常

相关接口：

- `GET /v1/logs`
- `GET /v1/logs/summary`

日志摘要目前包含：

- 总日志数
- `INFO` 数量
- `WARNING` 数量
- `ERROR` 数量
- 出现失败的任务数量

### 5. 模板系统

模板系统用于沉淀常见站点配置，减少重复配置成本。

目前支持：

- 查看模板列表
- 新建模板
- 编辑模板
- 删除模板
- 记录模板使用次数
- 记录最近使用时间
- 从模板直接创建任务
- 从已有任务反向保存为模板

相关接口：

- `GET /v1/templates/tasks`
- `POST /v1/templates/tasks`
- `PUT /v1/templates/tasks/{template_id}`
- `DELETE /v1/templates/tasks/{template_id}`
- `POST /v1/templates/tasks/{template_id}/use`

模板当前存储在：

- `server/storage/templates/task_templates.json`

这样设计的好处是：

- 不需要额外数据库迁移
- 可直接查看模板文件
- 后续迁移到数据库也很容易

## 五、抓取流程说明

单次任务运行的处理链路如下：

```text
Task
  -> Downloader
  -> Parser
  -> Cleaner
  -> Validator
  -> Deduplicate
  -> Save
  -> Snapshot
```

当前行为说明：

- 优先静态抓取，失败后回退到动态抓取
- 优先按解析规则解析，失败后回退到 readability
- 对清洗后的正文做 SHA-256 去重
- 将原始页面保存为 HTML 快照
- 全过程写入日志

## 六、前端能力说明

当前 Flutter 控制台已经不是占位骨架，而是具备实际操作价值的管理界面。

目前已经实现：

### 1. 仪表盘

- 今日新增公告数
- 关键词命中统计
- 来源站点分布
- 高价值公告
- 最近公告

### 2. 公告中心

- 公告列表
- 公告详情
- 快照查看
- 关键词命中展示

### 3. 任务管理

- 任务列表
- 搜索与筛选
- 创建 / 编辑 / 删除
- 启用 / 停用
- 立即执行
- 运行状态追踪
- 自动刷新
- 最近日志查看
- 从任务保存为模板

### 4. 全局日志面板

- 日志分页
- 按任务 ID 筛选
- 按级别筛选
- 关键词搜索
- 错误任务快捷修复入口
- 日志摘要统计

### 5. 来源站点模板管理

- 模板目录展示
- 模板新增 / 编辑 / 删除
- 模板标签
- 模板使用次数与最近使用时间
- 一键套用模板创建任务

更详细的前端说明请看：[frontend/README.md](frontend/README.md)

### 6. 登录说明

当前系统带有后端登录接口，启动后会自动创建默认管理员账号（与 `server/app/core/config.py` 中 `Settings` 一致）：

- 用户名：`madao`
- 初始密码：`666666`

登录成功后会返回会话 token，前端会在浏览器中保存该会话，刷新页面也可以继续保持登录状态。

## 七、本地启动

### 0. Windows 一键启动（推荐）

```powershell
cd crawler_system
powershell -ExecutionPolicy Bypass -File .\scripts\dev-up.ps1
```

该脚本会自动：

- 清理固定端口监听（后端 `8000`、前端 `8093`）
- 启动后端（`uvicorn`）和前端（`flutter web-server`）
- 输出最终访问地址

如需自定义端口，可传参：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev-up.ps1 -BackendPort 8001 -FrontendPort 8094
```

一键停止（默认停止 `8000` 和 `8093`）：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev-down.ps1
```

### 1. 启动后端

```bash
cd server
python -m venv ..\.venv
..\.venv\Scripts\python -m pip install -r requirements.txt
python -m playwright install chromium
..\.venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

首次启动时，系统会自动：

- 创建 `server/data.db`
- 建表
- 创建运行所需目录
- 启动调度器
- 在任务表为空时插入示例任务
- 初始化模板存储文件

### 2. 启动前端

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

### 3. 自动化测试（可选）

```bash
cd server
..\.venv\Scripts\python -m pip install -r requirements-dev.txt
..\.venv\Scripts\python -m pytest -q
```

```bash
cd frontend
flutter pub get
flutter analyze
flutter test
```

## 八、Docker 启动

在项目根目录执行：

```bash
docker compose up --build
```

默认后端地址：

```text
http://127.0.0.1:8000
```

## 九、数据与存储位置

- SQLite 数据库：`server/data.db`
- 页面快照：`server/storage/snapshots`
- 导出目录：`server/storage/exports`
- 模板目录：`server/storage/templates`

注意：

- 系统实际使用的数据库是 `crawler_system/server/data.db`
- 项目根目录外层那个 `data.db` 不是后端默认数据库

## 十、统一响应格式

所有接口统一使用以下响应包裹结构：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

分页接口统一支持：

```text
?page=1&page_size=20
```

## 十一、当前已完成与下一步建议

### 已完成

- 后端任务链路打通
- 采集数据入库与快照保存
- 任务状态跟踪
- 日志系统与日志摘要
- Flutter 运维控制台
- 模板管理与模板使用统计
- 模板与任务双向流转
- 采集数据 CSV 导出、模板目录搜索与排序
- 后端 `pytest`（含 HTTP 集成）与前端 `flutter test`（含 `ApiClient` / HTTP 仓库 Mock）

### 建议下一步

- 支持“列表页 -> 详情页”的多页抓取
- 模板热门度、保存前校验与更丰富的解析测试
- 更完整的端到端（浏览器）或契约测试

## 十二、适合谁来继续维护

这个项目现在已经比较适合：

- 后端工程师继续补采集能力
- 前端工程师继续补体验与可视化
- 业务运营人员通过模板和任务面板直接参与维护

如果你准备继续扩展它，建议优先沿着“模板治理”和“多页抓取”两条线推进。
