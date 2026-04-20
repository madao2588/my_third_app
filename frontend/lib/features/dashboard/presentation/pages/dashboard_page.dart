import 'package:flutter/material.dart';

import '../../../../core/network/api_client.dart';
import '../../../../core/utils/date_formatter.dart';
import '../../../../core/widgets/async_error_panel.dart';
import '../../data/models/dashboard_models.dart';
import '../../data/repositories/http_dashboard_repository.dart';
import '../../../notices/data/models/notice_models.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  late final HttpDashboardRepository _repository;
  late Future<DashboardOverviewModel> _future;

  @override
  void initState() {
    super.initState();
    _repository = HttpDashboardRepository(apiClient: ApiClient());
    _future = _repository.fetchOverview();
  }

  Future<void> _refresh() async {
    setState(() {
      _future = _repository.fetchOverview();
    });
    await _future;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<DashboardOverviewModel>(
      future: _future,
      builder: (context, snapshot) {
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _DashboardHero(
                lastUpdatedAt: snapshot.data?.lastUpdatedAt,
                runtime: snapshot.data?.runtime ??
                    DashboardRuntimeModel.fromJson(null),
                onRefresh: _refresh,
              ),
              const SizedBox(height: 16),
              Expanded(
                child: _buildBody(context, snapshot),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildBody(
    BuildContext context,
    AsyncSnapshot<DashboardOverviewModel> snapshot,
  ) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(28),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 16),
              Text('正在刷新首页看板...'),
            ],
          ),
        ),
      );
    }

    if (snapshot.hasError) {
      return AsyncErrorPanel(
        error: snapshot.error!,
        title: '加载首页看板失败',
        onRetry: _refresh,
      );
    }

    final data = snapshot.data;
    if (data == null) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(20),
          child: Text('暂无首页数据'),
        ),
      );
    }

    return LayoutBuilder(
      builder: (context, constraints) {
        final isWide = constraints.maxWidth >= 1100;
        final metrics = [
          _MetricCard(
            title: '今日新增公告',
            value: '${data.metrics.todayNewNotices}',
            subtitle: '当前采集窗口内新增内容',
            icon: Icons.notifications_active_outlined,
            accentColor: const Color(0xFF1E4F8A),
          ),
          _MetricCard(
            title: '关键词命中公告',
            value: '${data.metrics.keywordHitNotices}',
            subtitle: '有明确业务线索的公告',
            icon: Icons.local_offer_outlined,
            accentColor: const Color(0xFF117A65),
          ),
          _MetricCard(
            title: '监测站点数',
            value: '${data.metrics.monitoringSiteCount}',
            subtitle: '当前纳入监控的站点',
            icon: Icons.language_outlined,
            accentColor: const Color(0xFF2D6CDF),
          ),
          _MetricCard(
            title: '高优先级公告',
            value: '${data.metrics.highPriorityNotices}',
            subtitle: '需要重点关注的线索',
            icon: Icons.flag_outlined,
            accentColor: const Color(0xFFC45A1A),
          ),
        ];

        return Scrollbar(
          thumbVisibility: true,
          child: ListView(
            children: [
              LayoutBuilder(
                builder: (context, metricsConstraints) {
                  final cardWidth = metricsConstraints.maxWidth >= 1200
                      ? (metricsConstraints.maxWidth - 48) / 4
                      : metricsConstraints.maxWidth >= 760
                          ? (metricsConstraints.maxWidth - 16) / 2
                          : metricsConstraints.maxWidth;
                  return Wrap(
                    spacing: 16,
                    runSpacing: 16,
                    children: metrics
                        .map(
                          (metric) => SizedBox(width: cardWidth, child: metric),
                        )
                        .toList(),
                  );
                },
              ),
              const SizedBox(height: 18),
              if (isWide)
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      flex: 3,
                      child: _SectionCard(
                        title: '高价值公告',
                        action: Text(
                          '共 ${data.highValueNotices.length} 条',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                        child: _NoticeList(notices: data.highValueNotices),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      flex: 2,
                      child: Column(
                        children: [
                          _SectionCard(
                            title: '关键词热度',
                            child: _KeywordHeatGrid(items: data.keywordHeat),
                          ),
                          const SizedBox(height: 16),
                          _SectionCard(
                            title: '最近公告',
                            child: _RecentNoticeList(items: data.recentNotices),
                          ),
                        ],
                      ),
                    ),
                  ],
                )
              else ...[
                _SectionCard(
                  title: '高价值公告',
                  action: Text(
                    '共 ${data.highValueNotices.length} 条',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  child: _NoticeList(notices: data.highValueNotices),
                ),
                const SizedBox(height: 16),
                _SectionCard(
                  title: '关键词热度',
                  child: _KeywordHeatGrid(items: data.keywordHeat),
                ),
                const SizedBox(height: 16),
                _SectionCard(
                  title: '最近公告',
                  child: _RecentNoticeList(items: data.recentNotices),
                ),
              ],
              const SizedBox(height: 16),
              LayoutBuilder(
                builder: (context, sectionConstraints) {
                  final sideBySide = sectionConstraints.maxWidth >= 980;
                  final sourceCard = _SectionCard(
                    title: '来源站点分布',
                    child: Column(
                      children: data.sourceDistribution
                          .map(
                            (item) => Padding(
                              padding: const EdgeInsets.only(bottom: 12),
                              child: _SourceDistributionRow(item: item),
                            ),
                          )
                          .toList(),
                    ),
                  );

                  final summaryCard = _SectionCard(
                    title: '运行摘要',
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '当前看板聚焦高质量线索、关键词命中与站点覆盖，适合用于每日巡检和任务调度复盘。',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 16),
                        const Wrap(
                          spacing: 10,
                          runSpacing: 10,
                          children: [
                            _InfoChip(
                              label: '高价值优先',
                              color: Color(0xFFEAF3FF),
                              textColor: Color(0xFF1E4F8A),
                            ),
                            _InfoChip(
                              label: '关键词驱动',
                              color: Color(0xFFE7FBF5),
                              textColor: Color(0xFF117A65),
                            ),
                            _InfoChip(
                              label: '支持持续巡检',
                              color: Color(0xFFFFF4E8),
                              textColor: Color(0xFFC45A1A),
                            ),
                          ],
                        ),
                      ],
                    ),
                  );

                  if (!sideBySide) {
                    return Column(
                      children: [
                        sourceCard,
                        const SizedBox(height: 16),
                        summaryCard,
                      ],
                    );
                  }

                  return Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(child: sourceCard),
                      const SizedBox(width: 16),
                      Expanded(child: summaryCard),
                    ],
                  );
                },
              ),
            ],
          ),
        );
      },
    );
  }
}

class _MetricCard extends StatelessWidget {
  final String title;
  final String value;
  final String subtitle;
  final IconData icon;
  final Color accentColor;

  const _MetricCard({
    required this.title,
    required this.value,
    required this.subtitle,
    required this.icon,
    required this.accentColor,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              accentColor.withValues(alpha: 0.08),
              Colors.white,
            ],
          ),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  width: 42,
                  height: 42,
                  decoration: BoxDecoration(
                    color: accentColor.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Icon(icon, color: accentColor),
                ),
                const Spacer(),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF2F6FC),
                    borderRadius: BorderRadius.circular(999),
                  ),
                  child: Text(
                    '实时',
                    style: Theme.of(context).textTheme.labelMedium?.copyWith(
                          color: accentColor,
                          fontWeight: FontWeight.w700,
                        ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Text(
              title,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 10),
            Text(
              value,
              style: Theme.of(context).textTheme.displaySmall?.copyWith(
                    color: const Color(0xFF0F223D),
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              subtitle,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  final String title;
  final Widget child;
  final Widget? action;

  const _SectionCard({
    required this.title,
    required this.child,
    this.action,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    title,
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ),
                if (action != null) action!,
              ],
            ),
            const SizedBox(height: 16),
            child,
          ],
        ),
      ),
    );
  }
}

class _DashboardHero extends StatelessWidget {
  final String? lastUpdatedAt;
  final DashboardRuntimeModel runtime;
  final Future<void> Function() onRefresh;

  const _DashboardHero({
    required this.lastUpdatedAt,
    required this.runtime,
    required this.onRefresh,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Color(0xFF1D4E89),
            Color(0xFF235F9B),
            Color(0xFF13786A),
          ],
        ),
        borderRadius: BorderRadius.circular(28),
        boxShadow: const [
          BoxShadow(
            color: Color(0x281D4E89),
            blurRadius: 30,
            offset: Offset(0, 16),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '首页看板',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: Colors.white,
                      ),
                ),
                const SizedBox(height: 10),
                Text(
                  '从新增公告、关键词命中、高优先级线索和来源分布，快速掌握今天的采集热度。',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: const Color(0xE6F3F8FF),
                      ),
                ),
                const SizedBox(height: 16),
                const Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: [
                    _InfoChip(
                      label: '实时巡检',
                      color: Color(0x1AFFFFFF),
                      textColor: Colors.white,
                      borderColor: Color(0x33FFFFFF),
                    ),
                    _InfoChip(
                      label: '模板驱动',
                      color: Color(0x1AFFFFFF),
                      textColor: Colors.white,
                      borderColor: Color(0x33FFFFFF),
                    ),
                    _InfoChip(
                      label: '任务闭环',
                      color: Color(0x1AFFFFFF),
                      textColor: Colors.white,
                      borderColor: Color(0x33FFFFFF),
                    ),
                  ],
                ),
                const SizedBox(height: 14),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    _InfoChip(
                      label: '数据库 · ${runtime.database}',
                      color: const Color(0x24FFFFFF),
                      textColor: Colors.white,
                      borderColor: const Color(0x44FFFFFF),
                    ),
                    _InfoChip(
                      label: '调度器 · ${runtime.scheduler}',
                      color: const Color(0x24FFFFFF),
                      textColor: Colors.white,
                      borderColor: const Color(0x44FFFFFF),
                    ),
                    _InfoChip(
                      label: '定时任务 · ${runtime.scheduledJobs}',
                      color: const Color(0x24FFFFFF),
                      textColor: Colors.white,
                      borderColor: const Color(0x44FFFFFF),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(width: 16),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              FilledButton.tonalIcon(
                onPressed: onRefresh,
                icon: const Icon(Icons.refresh),
                label: const Text('刷新'),
              ),
              const SizedBox(height: 12),
              _InfoChip(
                label: lastUpdatedAt == null || lastUpdatedAt!.isEmpty
                    ? '待更新'
                    : '更新于 ${DateFormatter.formatDateTime(lastUpdatedAt!)}',
                color: const Color(0x1AFFFFFF),
                textColor: Colors.white,
                borderColor: const Color(0x33FFFFFF),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _NoticeList extends StatelessWidget {
  final List<NoticeListItemModel> notices;

  const _NoticeList({required this.notices});

  @override
  Widget build(BuildContext context) {
    if (notices.isEmpty) {
      return const Padding(
        padding: EdgeInsets.symmetric(vertical: 8),
        child: Text('暂无高价值公告。'),
      );
    }

    return Column(
      children: notices
          .map(
            (item) => Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFF8FBFF),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFFE2EAF4)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(
                        child: Text(
                          item.title.isEmpty ? '未命名公告' : item.title,
                          style:
                              Theme.of(context).textTheme.titleMedium?.copyWith(
                                    height: 1.3,
                                  ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      _InfoChip(
                        label: '质量分 ${item.qualityScore}',
                        color: const Color(0xFFEAF3FF),
                        textColor: const Color(0xFF1E4F8A),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    item.summary.isEmpty ? '暂无摘要。' : item.summary,
                    style: Theme.of(context).textTheme.bodyMedium,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      _InfoChip(
                        label:
                            item.sourceSite.isEmpty ? '未知来源' : item.sourceSite,
                        color: const Color(0xFFF0F6FB),
                        textColor: const Color(0xFF2F425B),
                      ),
                      _InfoChip(
                        label: item.isHighPriority ? '高优先级' : '一般',
                        color: item.isHighPriority
                            ? const Color(0xFFFFF2E8)
                            : const Color(0xFFF0F6FB),
                        textColor: item.isHighPriority
                            ? const Color(0xFFC45A1A)
                            : const Color(0xFF2F425B),
                      ),
                      ...item.matchedKeywords.take(3).map(
                            (keyword) => _InfoChip(
                              label: keyword,
                              color: const Color(0xFFE7FBF5),
                              textColor: const Color(0xFF117A65),
                            ),
                          ),
                    ],
                  ),
                ],
              ),
            ),
          )
          .toList(),
    );
  }
}

class _RecentNoticeList extends StatelessWidget {
  final List<NoticeListItemModel> items;

  const _RecentNoticeList({required this.items});

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) {
      return const Padding(
        padding: EdgeInsets.symmetric(vertical: 8),
        child: Text('暂无最近公告。'),
      );
    }

    return Column(
      children: items
          .take(5)
          .map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: const Color(0xFFEAF3FF),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: const Icon(
                      Icons.article_outlined,
                      color: Color(0xFF1E4F8A),
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          item.title.isEmpty ? '未命名公告' : item.title,
                          style: Theme.of(context).textTheme.titleMedium,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          item.sourceSite.isEmpty
                              ? '来源未知'
                              : '${item.sourceSite} · ${DateFormatter.formatShortDate(item.capturedAt)}',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          )
          .toList(),
    );
  }
}

class _KeywordHeatGrid extends StatelessWidget {
  final List<KeywordHeatItemModel> items;

  const _KeywordHeatGrid({required this.items});

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) {
      return const Padding(
        padding: EdgeInsets.symmetric(vertical: 8),
        child: Text('暂无关键词热度。'),
      );
    }

    return Wrap(
      spacing: 10,
      runSpacing: 10,
      children: items
          .map(
            (item) => Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
              decoration: BoxDecoration(
                color: const Color(0xFFF3F8FF),
                borderRadius: BorderRadius.circular(18),
                border: Border.all(color: const Color(0xFFE2EAF4)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    item.keyword,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${item.count} 次命中',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          )
          .toList(),
    );
  }
}

class _SourceDistributionRow extends StatelessWidget {
  final SourceDistributionItemModel item;

  const _SourceDistributionRow({required this.item});

  @override
  Widget build(BuildContext context) {
    final progress = (item.percentage / 100).clamp(0.0, 1.0);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Expanded(
              child: Text(
                item.sourceSite.isEmpty ? '未知来源' : item.sourceSite,
                style: Theme.of(context).textTheme.titleMedium,
              ),
            ),
            Text(
              '${item.noticeCount} 条',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
        const SizedBox(height: 8),
        ClipRRect(
          borderRadius: BorderRadius.circular(999),
          child: LinearProgressIndicator(
            value: progress,
            minHeight: 10,
            backgroundColor: const Color(0xFFE8EEF7),
            valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF1E4F8A)),
          ),
        ),
        const SizedBox(height: 6),
        Text(
          '${item.percentage.toStringAsFixed(1)}%',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
      ],
    );
  }
}

class _InfoChip extends StatelessWidget {
  final String label;
  final Color color;
  final Color textColor;
  final Color? borderColor;

  const _InfoChip({
    required this.label,
    required this.color,
    required this.textColor,
    this.borderColor,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(999),
        border: Border.all(
          color: borderColor ?? color.withValues(alpha: 0.2),
        ),
      ),
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: textColor,
              fontWeight: FontWeight.w700,
            ),
      ),
    );
  }
}
