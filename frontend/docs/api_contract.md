# 前后端接口对齐说明

## 一、对齐目标

为了让 Flutter 前端按业务模块开发，后端新增了一组更贴近页面语义的业务接口。

这些接口不会替代原有技术接口，而是作为前端优先使用的联调入口。

## 二、推荐前端使用的接口

### 1. 首页看板

- `GET /v1/dashboard/overview`

返回内容包含：
- 核心指标
- 高价值公告
- 最新公告
- 关键词热度
- 来源网站分布
- 最后更新时间

### 2. 公告中心

- `GET /v1/notices`
- `GET /v1/notices/{id}`
- `GET /v1/notices/{id}/snapshot`

返回内容包含：
- 标题
- 摘要
- 来源网站
- 原文链接
- 抓取时间
- 命中关键词
- 质量分
- 是否高优先级

### 3. 系统管理

暂时继续复用原有接口：
- `GET /v1/tasks`
- `POST /v1/tasks/{id}/run`
- `GET /v1/logs`
- `GET /v1/stats/overview`

## 三、当前前后端映射

- 首页看板 -> `GET /v1/dashboard/overview`
- 公告中心列表 -> `GET /v1/notices`
- 公告详情 -> `GET /v1/notices/{id}`
- 公告快照 -> `GET /v1/notices/{id}/snapshot`
- 监测任务 -> `GET /v1/tasks`
- 手动运行任务 -> `POST /v1/tasks/{id}/run`
- 运行日志 -> `GET /v1/logs`

## 四、当前仍是第二阶段的模块

以下页面后端还没有正式业务接口，先保留设计，不进入联调：
- 关键词规则
- 来源网站

后续建议补充：
- `GET /v1/keyword-rules`
- `POST /v1/keyword-rules`
- `GET /v1/source-sites`
- `POST /v1/source-sites`

## 五、字段说明

### Notice

- `title`: 公告标题
- `summary`: 公告摘要
- `source_site`: 来源网站域名
- `source_url`: 原文链接
- `published_at`: 公告发布时间
- `captured_at`: 系统抓取时间
- `quality_score`: 质量评分
- `matched_keywords`: 命中关键词
- `is_high_priority`: 是否高优先级
- `task_id`: 关联监测任务

说明：
- 当前后端尚未稳定提取真实公告发布时间，因此 `published_at` 可能为空
- 第一阶段前端建议优先展示 `captured_at`

## 六、Flutter 当前已对齐的代码位置

前端已预留以下结构用于联调：

- `lib/core/constants/api_paths.dart`
- `lib/features/dashboard/data/models/dashboard_models.dart`
- `lib/features/notices/data/models/notice_models.dart`
- `lib/features/dashboard/data/repositories/dashboard_repository.dart`
- `lib/features/notices/data/repositories/notice_repository.dart`

说明：
- 当前只是数据结构和仓储接口占位
- 已补充 `ApiClient` 与 HTTP Repository 骨架
- 尚未接入页面状态管理与真实页面渲染
