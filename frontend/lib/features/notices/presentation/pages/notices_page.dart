import 'dart:async';
import 'package:flutter/material.dart';

import '../../../../core/network/api_client.dart';
import '../../../../core/utils/date_formatter.dart';
import '../../../../shared/models/page_data.dart';
import '../../data/models/notice_models.dart';
import '../../data/repositories/http_notice_repository.dart';
import 'package:url_launcher/url_launcher.dart';

class NoticesPage extends StatefulWidget {
  const NoticesPage({super.key});

  @override
  State<NoticesPage> createState() => _NoticesPageState();
}

class _NoticesPageState extends State<NoticesPage> {
  late final HttpNoticeRepository _repository;
  late Future<PageData<NoticeListItemModel>> _noticesFuture;
  Future<NoticeDetailModel>? _detailFuture;
  int? _selectedNoticeId;
  Timer? _autoRefreshTimer;
  final ScrollController _horizontalScrollController = ScrollController();
  final TextEditingController _searchController = TextEditingController();

  int _currentPage = 1;
  final int _pageSize = 20;
  String? _keyword;

  @override
  void dispose() {
    _autoRefreshTimer?.cancel();
    _searchController.dispose();
    _horizontalScrollController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    _repository = HttpNoticeRepository(apiClient: ApiClient());
    _noticesFuture = _fetchPage();
    _startAutoRefresh();
  }

  Future<PageData<NoticeListItemModel>> _fetchPage() {
    return _repository.fetchNotices(
      page: _currentPage,
      pageSize: _pageSize,
      keyword: _keyword,
    );
  }

  void _onSearch(String keyword) {
    setState(() {
      _keyword = keyword;
      _currentPage = 1;
      _noticesFuture = _fetchPage();
    });
  }

  void _onPageChanged(int newPage) {
    setState(() {
      _currentPage = newPage;
      _noticesFuture = _fetchPage();
    });
  }

  Future<void> _refresh() async {
    setState(() {
      _currentPage = 1;
      _noticesFuture = _fetchPage();
    });
    await _noticesFuture;
  }

  Future<void> _refreshCurrentPage() async {
    setState(() {
      _noticesFuture = _fetchPage();
      if (_selectedNoticeId != null) {
        _detailFuture = _repository.fetchNoticeDetail(_selectedNoticeId!);
      }
    });
    await _noticesFuture;
  }

  void _startAutoRefresh() {
    _autoRefreshTimer?.cancel();
    _autoRefreshTimer = Timer.periodic(const Duration(seconds: 10), (_) async {
      if (!mounted) {
        return;
      }
      await _refreshCurrentPage();
    });
  }

  void _selectNotice(int noticeId) {
    if (_selectedNoticeId == noticeId) {
      return;
    }
    setState(() {
      _selectedNoticeId = noticeId;
      _detailFuture = _repository.fetchNoticeDetail(noticeId);
    });
  }

  Future<void> _openSnapshot(
    BuildContext context,
    NoticeDetailModel detail, [
    String? keywordToHighlight,
  ]) async {
    final messenger = ScaffoldMessenger.of(context);
    try {
      final snapshot = await _repository.fetchSnapshot(detail.id);
      if (!context.mounted) {
        return;
      }
      await showDialog<void>(
        context: context,
        builder: (context) {
          return _SnapshotViewerDialog(
            content: snapshot.content,
            keywordToHighlight: keywordToHighlight,
          );
        },
      );
    } catch (error) {
      messenger.showSnackBar(
        SnackBar(content: Text('加载快照失败：$error')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<PageData<NoticeListItemModel>>(
      future: _noticesFuture,
      builder: (context, snapshot) {
        final items = snapshot.data?.items ?? const <NoticeListItemModel>[];
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _NoticeHero(
                items: items,
                onRefresh: _refresh,
              ),
              const SizedBox(height: 16),
              _NoticeFilterBar(
                searchController: _searchController,
                onSearch: _onSearch,
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
    AsyncSnapshot<PageData<NoticeListItemModel>> snapshot,
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
              Text('正在刷新公告列表...'),
            ],
          ),
        ),
      );
    }

    if (snapshot.hasError) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Text('加载公告列表失败：${snapshot.error}'),
        ),
      );
    }

    final items = snapshot.data?.items ?? const <NoticeListItemModel>[];
    if (items.isEmpty) {
      return _EmptyStateCard(
        icon: Icons.inbox_outlined,
        title: '暂无公告数据',
        description: '当前没有可展示的公告，等采集任务再次运行后这里会自动更新。',
        actionLabel: '刷新',
        onAction: _refresh,
      );
    }

    final selectedNotice = _syncSelection(items);

    final totalPages = (snapshot.data?.total ?? 0) / _pageSize;
    final maxPage = totalPages.ceil();
    final effectiveMaxPage = maxPage == 0 && items.isNotEmpty ? 1 : maxPage;

    final paginationRow = Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
          icon: const Icon(Icons.chevron_left),
          onPressed:
              _currentPage > 1 ? () => _onPageChanged(_currentPage - 1) : null,
        ),
        Text('第 $_currentPage 页 / 共 $effectiveMaxPage 页'),
        IconButton(
          icon: const Icon(Icons.chevron_right),
          onPressed: _currentPage < effectiveMaxPage
              ? () => _onPageChanged(_currentPage + 1)
              : null,
        ),
      ],
    );

    return LayoutBuilder(
      builder: (context, constraints) {
        final content = Column(
          children: [
            Expanded(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 5,
                    child: _NoticeListOnly(
                      items: items,
                      selectedNoticeId: _selectedNoticeId,
                      onSelect: _selectNotice,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    flex: 4,
                    child: _NoticeDetailPanel(
                      noticeId: selectedNotice.id,
                      detailFuture: _detailFuture!,
                      onOpenSnapshot: _openSnapshot,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            paginationRow,
          ],
        );

        if (constraints.maxWidth < 1000) {
          return Scrollbar(
            controller: _horizontalScrollController,
            interactive: true,
            thumbVisibility: true,
            scrollbarOrientation: ScrollbarOrientation.bottom,
            child: SingleChildScrollView(
              controller: _horizontalScrollController,
              scrollDirection: Axis.horizontal,
              child: SizedBox(
                width: 1000,
                child: content,
              ),
            ),
          );
        }

        return content;
      },
    );
  }

  NoticeListItemModel _syncSelection(List<NoticeListItemModel> items) {
    for (final item in items) {
      if (item.id == _selectedNoticeId && _detailFuture != null) {
        return item;
      }
    }

    final fallback = items.first;
    _selectedNoticeId = fallback.id;
    _detailFuture = _repository.fetchNoticeDetail(fallback.id);
    return fallback;
  }
}

class _NoticeHero extends StatelessWidget {
  final List<NoticeListItemModel> items;
  final Future<void> Function() onRefresh;

  const _NoticeHero({
    required this.items,
    required this.onRefresh,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isCompact = constraints.maxWidth < 760;
        final content = Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '公告中心',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    color: Colors.white,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              '按来源、关键词和优先级快速浏览采集结果，左侧筛选线索，右侧深入查看公告详情与快照。',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: const Color(0xE6F3F8FF),
                  ),
            ),
            const SizedBox(height: 16),
            _NoticeSummaryBar(items: items),
          ],
        );

        final actions = Column(
          crossAxisAlignment:
              isCompact ? CrossAxisAlignment.start : CrossAxisAlignment.end,
          children: [
            FilledButton.tonalIcon(
              onPressed: onRefresh,
              icon: const Icon(Icons.refresh),
              label: const Text('刷新'),
            ),
            const SizedBox(height: 12),
            _InfoPill(
              label: '聚焦采集结果',
              value: '${items.length} 条',
            ),
          ],
        );

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
          child: isCompact
              ? Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    content,
                    const SizedBox(height: 16),
                    actions,
                  ],
                )
              : Row(
                  children: [
                    Expanded(child: content),
                    const SizedBox(width: 16),
                    actions,
                  ],
                ),
        );
      },
    );
  }
}

class _NoticeSummaryBar extends StatelessWidget {
  final List<NoticeListItemModel> items;

  const _NoticeSummaryBar({required this.items});

  @override
  Widget build(BuildContext context) {
    final highPriority = items.where((item) => item.isHighPriority).length;
    final keywordHits =
        items.where((item) => item.matchedKeywords.isNotEmpty).length;
    final averageQuality = items.isEmpty
        ? 0
        : (items.fold<int>(0, (sum, item) => sum + item.qualityScore) /
                items.length)
            .round();

    return Wrap(
      spacing: 16,
      runSpacing: 16,
      children: [
        _NoticeMetricCard(
          title: '公告总数',
          value: '${items.length}',
          icon: Icons.article_outlined,
          accentColor: const Color(0xFF1E4F8A),
        ),
        _NoticeMetricCard(
          title: '高优先级',
          value: '$highPriority',
          icon: Icons.flag_outlined,
          accentColor: const Color(0xFFC45A1A),
        ),
        _NoticeMetricCard(
          title: '关键词命中',
          value: '$keywordHits',
          icon: Icons.local_offer_outlined,
          accentColor: const Color(0xFF117A65),
        ),
        _NoticeMetricCard(
          title: '平均质量分',
          value: '$averageQuality',
          icon: Icons.assessment_outlined,
          accentColor: const Color(0xFF2D6CDF),
        ),
      ],
    );
  }
}

class _EmptyStateCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;
  final String actionLabel;
  final Future<void> Function() onAction;

  const _EmptyStateCard({
    required this.icon,
    required this.title,
    required this.description,
    required this.actionLabel,
    required this.onAction,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(28),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 56,
              height: 56,
              decoration: BoxDecoration(
                color: const Color(0xFFEAF3FF),
                borderRadius: BorderRadius.circular(18),
              ),
              child: Icon(icon, color: const Color(0xFF1E4F8A)),
            ),
            const SizedBox(height: 18),
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 10),
            Text(description, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 18),
            FilledButton.tonalIcon(
              onPressed: onAction,
              icon: const Icon(Icons.refresh),
              label: Text(actionLabel),
            ),
          ],
        ),
      ),
    );
  }
}

class _NoticeMetricCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color accentColor;

  const _NoticeMetricCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.accentColor,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 190,
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
          borderRadius: BorderRadius.circular(20),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: accentColor.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Icon(icon, color: accentColor),
                  ),
                  const Spacer(),
                  _MetricPill(accentColor: accentColor),
                ],
              ),
              const SizedBox(height: 14),
              Text(
                title,
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 8),
              Text(
                value,
                style: Theme.of(context).textTheme.displaySmall?.copyWith(
                      color: const Color(0xFF0F223D),
                    ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MetricPill extends StatelessWidget {
  final Color accentColor;

  const _MetricPill({required this.accentColor});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
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
    );
  }
}

class _NoticeFilterBar extends StatefulWidget {
  final TextEditingController searchController;
  final ValueChanged<String> onSearch;

  const _NoticeFilterBar({
    required this.searchController,
    required this.onSearch,
  });

  @override
  State<_NoticeFilterBar> createState() => _NoticeFilterBarState();
}

class _NoticeFilterBarState extends State<_NoticeFilterBar> {
  Timer? _debounceTimer;

  void _onQueryChanged(String query) {
    if (_debounceTimer?.isActive ?? false) _debounceTimer!.cancel();
    _debounceTimer = Timer(const Duration(milliseconds: 500), () {
      widget.onSearch(query);
    });
  }

  @override
  void dispose() {
    _debounceTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isCompact = constraints.maxWidth < 760;

        final searchField = TextField(
          controller: widget.searchController,
          onChanged: _onQueryChanged,
          decoration: InputDecoration(
            labelText: '关键词搜索',
            hintText: '输入内容，回车或自动搜索',
            prefixIcon: const Icon(Icons.search),
            suffixIcon: widget.searchController.text.isNotEmpty
                ? IconButton(
                    icon: const Icon(Icons.clear),
                    onPressed: () {
                      widget.searchController.clear();
                      _onQueryChanged('');
                    },
                  )
                : null,
          ),
        );

        final statusChip = Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          decoration: BoxDecoration(
            color: const Color(0xFFEAF3FF),
            borderRadius: BorderRadius.circular(18),
          ),
          child: const Text(
            '筛选功能即将增强',
            style: TextStyle(
              color: Color(0xFF1E4F8A),
              fontWeight: FontWeight.w600,
            ),
          ),
        );

        return Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: isCompact
                ? Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      searchField,
                      const SizedBox(height: 12),
                      statusChip,
                    ],
                  )
                : Row(
                    children: [
                      Expanded(
                          child: TextField(
                        controller: widget.searchController,
                        onChanged: _onQueryChanged,
                        decoration: InputDecoration(
                          labelText: '关键词搜索',
                          hintText: '输入内容，回车或自动搜索',
                          prefixIcon: const Icon(Icons.search),
                          suffixIcon: widget.searchController.text.isNotEmpty
                              ? IconButton(
                                  icon: const Icon(Icons.clear),
                                  onPressed: () {
                                    widget.searchController.clear();
                                    _onQueryChanged('');
                                  },
                                )
                              : null,
                        ),
                      )),
                      const SizedBox(width: 12),
                      statusChip,
                    ],
                  ),
          ),
        );
      },
    );
  }
}

class _NoticeListOnly extends StatefulWidget {
  final List<NoticeListItemModel> items;
  final int? selectedNoticeId;
  final ValueChanged<int> onSelect;

  const _NoticeListOnly({
    required this.items,
    required this.selectedNoticeId,
    required this.onSelect,
  });

  @override
  State<_NoticeListOnly> createState() => _NoticeListOnlyState();
}

class _NoticeListOnlyState extends State<_NoticeListOnly> {
  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Scrollbar(
        controller: _scrollController,
        interactive: true,
        thumbVisibility: true,
        child: ListView.separated(
          controller: _scrollController,
          padding: const EdgeInsets.all(12),
          itemCount: widget.items.length,
          separatorBuilder: (_, __) => const SizedBox(height: 10),
          itemBuilder: (context, index) {
            final item = widget.items[index];
            final selected = item.id == widget.selectedNoticeId;

            return AnimatedContainer(
              duration: const Duration(milliseconds: 180),
              decoration: BoxDecoration(
                color: selected
                    ? const Color(0xFFEAF2FF)
                    : const Color(0xFFFDFEFF),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: selected
                      ? const Color(0xFFBFD3F8)
                      : const Color(0xFFE4EBF5),
                ),
              ),
              child: InkWell(
                borderRadius: BorderRadius.circular(20),
                onTap: () => widget.onSelect(item.id),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Expanded(
                            child: Text(
                              item.title.isEmpty ? '未命名公告' : item.title,
                              style: Theme.of(context).textTheme.titleMedium,
                            ),
                          ),
                          const SizedBox(width: 12),
                          _PriorityPill(isHighPriority: item.isHighPriority),
                        ],
                      ),
                      if (item.summary.isNotEmpty) ...[
                        const SizedBox(height: 10),
                        Text(
                          item.summary,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                      ],
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          _InfoPill(label: '来源', value: item.sourceSite),
                          _InfoPill(
                            label: '采集时间',
                            value: DateFormatter.formatDateTime(item.capturedAt),
                          ),
                          _InfoPill(
                              label: '质量分', value: '${item.qualityScore}'),
                        ],
                      ),
                      if (item.matchedKeywords.isNotEmpty) ...[
                        const SizedBox(height: 12),
                        Wrap(
                          spacing: 6,
                          runSpacing: 6,
                          children: item.matchedKeywords
                              .map((keyword) => Chip(label: Text(keyword)))
                              .toList(),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _NoticeDetailPanel extends StatefulWidget {
  final int noticeId;
  final Future<NoticeDetailModel> detailFuture;
  final Future<void> Function(BuildContext, NoticeDetailModel, [String?])
      onOpenSnapshot;

  const _NoticeDetailPanel({
    required this.noticeId,
    required this.detailFuture,
    required this.onOpenSnapshot,
  });

  @override
  State<_NoticeDetailPanel> createState() => _NoticeDetailPanelState();
}

class _NoticeDetailPanelState extends State<_NoticeDetailPanel> {
  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<NoticeDetailModel>(
      key: ValueKey(widget.noticeId),
      future: widget.detailFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Card(
            child: Center(child: CircularProgressIndicator()),
          );
        }

        if (snapshot.hasError) {
          return Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Text('加载公告详情失败：${snapshot.error}'),
            ),
          );
        }

        final detail = snapshot.data;
        if (detail == null) {
          return const Card(
            child: Padding(
              padding: EdgeInsets.all(20),
              child: Text('暂无公告详情'),
            ),
          );
        }

        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Scrollbar(
              controller: _scrollController,
              interactive: true,
              thumbVisibility: true,
              child: ListView(
                controller: _scrollController,
                padding: EdgeInsets.zero,
                children: [
                  Text(
                    detail.title.isEmpty ? '未命名公告' : detail.title,
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 12,
                    runSpacing: 8,
                    children: [
                      _MetaTag(label: '来源站点', value: detail.sourceSite),
                      _MetaTag(
                        label: '采集时间',
                        value: DateFormatter.formatDateTime(detail.capturedAt),
                      ),
                      _MetaTag(label: '质量分', value: '${detail.qualityScore}'),
                      _MetaTag(
                        label: '发布时间',
                        value: detail.publishedAt == null
                            ? '暂无'
                            : DateFormatter.formatDateTime(
                                detail.publishedAt,
                                fallback: '暂无',
                              ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),
                  SelectableText(
                    detail.sourceUrl,
                    style: const TextStyle(
                      color: Color(0xFF1F4B99),
                      decoration: TextDecoration.underline,
                    ),
                  ),
                  if (detail.matchedKeywords.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: detail.matchedKeywords
                          .map((keyword) => ActionChip(
                                label: Text(keyword),
                                avatar: const Icon(Icons.search, size: 16),
                                onPressed: () => widget.onOpenSnapshot(
                                    context, detail, keyword),
                                tooltip: '在快照中查找此关键词',
                              ))
                          .toList(),
                    ),
                  ],
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      FilledButton.tonal(
                        onPressed: () => widget.onOpenSnapshot(context, detail),
                        child: const Text('查看快照'),
                      ),
                      const SizedBox(width: 12),
                      if (detail.sourceUrl.isNotEmpty)
                        OutlinedButton.icon(
                          onPressed: () async {
                            final uri = Uri.parse(detail.sourceUrl);
                            try {
                              await launchUrl(uri,
                                  mode: LaunchMode.externalApplication);
                            } catch (e) {
                              if (context.mounted) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(content: Text('无法打开原文链接: $uri')),
                                );
                              }
                            }
                          },
                          icon: const Icon(Icons.open_in_browser, size: 16),
                          label: const Text('查看原文'),
                        )
                      else
                        const OutlinedButton(
                          onPressed: null,
                          child: Text('无原文链接'),
                        ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  Text(
                    '正文内容',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 10),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF7FAFD),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: const Color(0xFFE3EAF5)),
                    ),
                    child: Text(
                      detail.contentText.isEmpty
                          ? '当前暂无正文内容。'
                          : detail.contentText,
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

class _PriorityPill extends StatelessWidget {
  final bool isHighPriority;

  const _PriorityPill({
    required this.isHighPriority,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color:
            isHighPriority ? const Color(0xFFFDEDED) : const Color(0xFFF3F6FA),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        isHighPriority ? '高优先级' : '普通',
        style: TextStyle(
          color: isHighPriority
              ? const Color(0xFFB42318)
              : const Color(0xFF556A86),
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}

class _InfoPill extends StatelessWidget {
  final String label;
  final String value;

  const _InfoPill({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFFF5F8FC),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        '$label：$value',
        style: Theme.of(context).textTheme.bodySmall,
      ),
    );
  }
}

class _MetaTag extends StatelessWidget {
  final String label;
  final String value;

  const _MetaTag({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFFF3F6FA),
        borderRadius: BorderRadius.circular(12),
      ),
      child: RichText(
        text: TextSpan(
          style: DefaultTextStyle.of(context).style,
          children: [
            TextSpan(
              text: '$label：',
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
            TextSpan(text: value),
          ],
        ),
      ),
    );
  }
}

class _SnapshotViewerDialog extends StatefulWidget {
  final String content;
  final String? keywordToHighlight;

  const _SnapshotViewerDialog({
    required this.content,
    this.keywordToHighlight,
  });

  @override
  State<_SnapshotViewerDialog> createState() => _SnapshotViewerDialogState();
}

class _SnapshotViewerDialogState extends State<_SnapshotViewerDialog> {
  final GlobalKey _targetKey = GlobalKey();
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.keywordToHighlight != null &&
          widget.keywordToHighlight!.isNotEmpty &&
          _targetKey.currentContext != null) {
        Scrollable.ensureVisible(
          _targetKey.currentContext!,
          duration: const Duration(milliseconds: 300),
          alignment: 0.2,
        );
      }
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  List<InlineSpan> _buildSpans(String text, String? keyword) {
    if (keyword == null || keyword.isEmpty) {
      return [TextSpan(text: text)];
    }
    final spans = <InlineSpan>[];
    final lowerText = text.toLowerCase();
    final lowerKeyword = keyword.toLowerCase();
    int start = 0;
    int indexOfMatch;
    bool isFirst = true;

    while ((indexOfMatch = lowerText.indexOf(lowerKeyword, start)) != -1) {
      if (indexOfMatch > start) {
        spans.add(TextSpan(text: text.substring(start, indexOfMatch)));
      }
      final kwText =
          text.substring(indexOfMatch, indexOfMatch + keyword.length);

      if (isFirst) {
        spans.add(
          WidgetSpan(
            alignment: PlaceholderAlignment.middle,
            child: Container(
              key: _targetKey,
              color: Colors.yellow,
              child: Text(
                kwText,
                style: const TextStyle(
                    color: Colors.red, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        );
        isFirst = false;
      } else {
        spans.add(
          TextSpan(
            text: kwText,
            style: const TextStyle(
              backgroundColor: Colors.yellow,
              color: Colors.red,
              fontWeight: FontWeight.bold,
            ),
          ),
        );
      }
      start = indexOfMatch + keyword.length;
    }
    if (start < text.length) {
      spans.add(TextSpan(text: text.substring(start)));
    }
    return spans;
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('快照内容'),
      content: SizedBox(
        width: 720,
        child: Scrollbar(
          controller: _scrollController,
          interactive: true,
          thumbVisibility: true,
          child: SingleChildScrollView(
            controller: _scrollController,
            child: SelectableText.rich(
              TextSpan(
                children:
                    _buildSpans(widget.content, widget.keywordToHighlight),
              ),
            ),
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('关闭'),
        ),
      ],
    );
  }
}
