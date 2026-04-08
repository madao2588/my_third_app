import 'dart:async';

import 'package:flutter/material.dart';

import '../../../../core/network/api_client.dart';
import '../../../../shared/models/page_data.dart';
import '../../data/models/task_models.dart';
import '../../data/models/task_template_models.dart';
import '../../data/repositories/http_task_repository.dart';
import '../../data/repositories/http_template_repository.dart';

class SystemManagementPage extends StatefulWidget {
  final TaskTemplateModel? pendingTemplate;
  final VoidCallback? onPendingTemplateHandled;
  final Future<void> Function() onTemplatesChanged;
  final HttpTemplateRepository templateRepository;
  final List<TaskTemplateModel> templates;

  const SystemManagementPage({
    super.key,
    this.pendingTemplate,
    this.onPendingTemplateHandled,
    required this.onTemplatesChanged,
    required this.templateRepository,
    required this.templates,
  });

  @override
  State<SystemManagementPage> createState() => _SystemManagementPageState();
}

class _SystemManagementPageState extends State<SystemManagementPage> {
  static const _activeStatuses = {'queued', 'running'};

  late final HttpTaskRepository _repository;
  late Future<PageData<TaskListItemModel>> _tasksFuture;
  late Future<PageData<TaskLogItemModel>> _logsFuture;
  late Future<LogSummaryModel> _logSummaryFuture;
  late final TextEditingController _searchController;
  late final TextEditingController _logTaskIdController;
  late final TextEditingController _logSearchController;
  late final ScrollController _taskTableScrollController;
  Timer? _listPollingTimer;
  int _remainingPollTicks = 0;
  int _selectedTabIndex = 0;
  int _taskPage = 1;
  final int _taskPageSize = 20;
  int _logPage = 1;
  final int _logPageSize = 20;
  String _searchQuery = '';
  String _enabledFilter = 'all';
  String _resultFilter = 'all';
  String _logLevelFilter = 'all';
  String _logSearchQuery = '';

  @override
  void initState() {
    super.initState();
    _repository = HttpTaskRepository(apiClient: ApiClient());
    _searchController = TextEditingController();
    _logTaskIdController = TextEditingController();
    _logSearchController = TextEditingController();
    _taskTableScrollController = ScrollController();
    _tasksFuture = _fetchTasks();
    _logsFuture = _fetchLogs();
    _logSummaryFuture = _repository.fetchLogSummary();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _consumePendingTemplateIfNeeded();
    });
  }

  @override
  void didUpdateWidget(covariant SystemManagementPage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.pendingTemplate?.id != oldWidget.pendingTemplate?.id &&
        widget.pendingTemplate != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _consumePendingTemplateIfNeeded();
      });
    }
  }

  @override
  void dispose() {
    _searchController.dispose();
    _logTaskIdController.dispose();
    _logSearchController.dispose();
    _taskTableScrollController.dispose();
    _listPollingTimer?.cancel();
    super.dispose();
  }

  Future<void> _refresh() async {
    setState(() {
      _tasksFuture = _fetchTasks();
    });
    await _tasksFuture;
  }

  Future<void> _refreshLogs() async {
    setState(() {
      _logsFuture = _fetchLogs();
      _logSummaryFuture = _repository.fetchLogSummary();
    });
    await Future.wait([_logsFuture, _logSummaryFuture]);
  }

  Future<PageData<TaskListItemModel>> _fetchTasks() {
    return _repository.fetchTasks(page: _taskPage, pageSize: _taskPageSize);
  }

  Future<PageData<TaskLogItemModel>> _fetchLogs() {
    return _repository.fetchLogs(
      page: _logPage,
      pageSize: _logPageSize,
      taskId: _parseTaskIdFilter(),
      level: _logLevelFilter == 'all' ? null : _logLevelFilter,
    );
  }

  Future<void> _openTaskEditor([TaskListItemModel? task]) async {
    final saved = await showDialog<bool>(
      context: context,
      builder: (context) => _TaskEditorDialog(
        task: task,
        repository: _repository,
        templates: widget.templates,
      ),
    );

    if (saved == true && mounted) {
      await _refresh();
      _showMessage(task == null ? '任务已创建。' : '任务已更新。');
    }
  }

  Future<void> _openTaskEditorWithTemplate(TaskTemplateModel template) async {
    final saved = await showDialog<bool>(
      context: context,
      builder: (context) => _TaskEditorDialog(
        repository: _repository,
        initialTemplate: template,
        templates: widget.templates,
      ),
    );

    widget.onPendingTemplateHandled?.call();

    if (saved == true && mounted) {
      await _refresh();
      _showMessage('已通过模板“${template.label}”创建任务。');
    }
  }

  Future<void> _consumePendingTemplateIfNeeded() async {
    final template = widget.pendingTemplate;
    if (template == null || !mounted) {
      return;
    }
    await _openTaskEditorWithTemplate(template);
  }

  Future<void> _toggleTask(TaskListItemModel task) async {
    try {
      await _repository.updateTask(
        task.id,
        TaskUpsertPayload(
          name: task.name,
          startUrl: task.startUrl,
          parserRules: _normalizeParserRules(task.parserRules),
          cronExpr: task.cronExpr,
          status: task.isEnabled ? 0 : 1,
        ),
      );
      if (!mounted) {
        return;
      }
      await _refresh();
      _showMessage(task.isEnabled ? '任务已停用。' : '任务已启用。');
    } catch (error) {
      _showMessage('更新任务失败：$error', isError: true);
    }
  }

  Future<void> _runTask(TaskListItemModel task) async {
    try {
      final result = await _repository.runTask(task.id);
      if (!mounted) {
        return;
      }
      _startListPolling();
      await _refresh();
      _showMessage('任务 ${result.taskId} 已进入队列，当前状态：${result.status}。');
    } catch (error) {
      _showMessage('运行任务失败：$error', isError: true);
    }
  }

  void _startListPolling() {
    _remainingPollTicks = 5;
    _listPollingTimer?.cancel();
    _listPollingTimer =
        Timer.periodic(const Duration(seconds: 3), (timer) async {
      if (!mounted) {
        timer.cancel();
        return;
      }

      await _refresh();
      _remainingPollTicks -= 1;

      final snapshot = await _tasksFuture;
      final hasActiveTasks = snapshot.items
          .any((task) => _activeStatuses.contains(task.lastRunStatus));

      if (_remainingPollTicks <= 0 || !hasActiveTasks) {
        timer.cancel();
        _listPollingTimer = null;
      }
    });
  }

  Future<void> _openTaskDetails(TaskListItemModel task) async {
    await showDialog<void>(
      context: context,
      builder: (context) => _TaskDetailsDialog(
        task: task,
        repository: _repository,
      ),
    );
  }

  Future<void> _deleteTask(TaskListItemModel task) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('删除任务？'),
        content: Text('这会永久删除“${task.name}”。'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('取消'),
          ),
          FilledButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('删除'),
          ),
        ],
      ),
    );

    if (confirmed != true) {
      return;
    }

    try {
      await _repository.deleteTask(task.id);
      if (!mounted) {
        return;
      }
      await _refresh();
      _showMessage('任务已删除。');
    } catch (error) {
      _showMessage('删除任务失败：$error', isError: true);
    }
  }

  Future<void> _openTaskDetailsById(int taskId) async {
    try {
      final task = await _repository.fetchTask(taskId);
      if (!mounted) {
        return;
      }
      await _openTaskDetails(task);
    } catch (error) {
      _showMessage('打开任务详情失败：$error', isError: true);
    }
  }

  Future<void> _openTaskEditorById(int taskId) async {
    try {
      final task = await _repository.fetchTask(taskId);
      if (!mounted) {
        return;
      }
      await _openTaskEditor(task);
    } catch (error) {
      _showMessage('打开任务编辑器失败：$error', isError: true);
    }
  }

  Future<void> _runTaskById(int taskId) async {
    try {
      final task = await _repository.fetchTask(taskId);
      if (!mounted) {
        return;
      }
      await _runTask(task);
      await _refreshLogs();
    } catch (error) {
      _showMessage('重新运行任务失败：$error', isError: true);
    }
  }

  Future<void> _saveTaskAsTemplate(TaskListItemModel task) async {
    final saved = await showDialog<bool>(
      context: context,
      builder: (context) => _SaveTaskAsTemplateDialog(
        task: task,
        repository: widget.templateRepository,
      ),
    );

    if (saved == true && mounted) {
      await widget.onTemplatesChanged();
      if (!mounted) {
        return;
      }
      _showMessage('已根据“${task.name}”生成模板。');
    }
  }

  void _showMessage(String message, {bool isError = false}) {
    if (!mounted) {
      return;
    }
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? const Color(0xFFB3261E) : null,
      ),
    );
  }

  String? _normalizeParserRules(String? value) {
    final trimmed = value?.trim();
    if (trimmed == null || trimmed.isEmpty) {
      return null;
    }
    return trimmed;
  }

  int? _parseTaskIdFilter() {
    final value = _logTaskIdController.text.trim();
    if (value.isEmpty) {
      return null;
    }
    return int.tryParse(value);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _SystemManagementHero(
            onRefreshTasks: _refresh,
            onRefreshLogs: _refreshLogs,
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: SegmentedButton<int>(
                segments: const [
                  ButtonSegment<int>(value: 0, label: Text('任务')),
                  ButtonSegment<int>(value: 1, label: Text('日志')),
                ],
                selected: {_selectedTabIndex},
                onSelectionChanged: (value) {
                  setState(() {
                    _selectedTabIndex = value.first;
                  });
                },
              ),
            ),
          ),
          const SizedBox(height: 16),
          Expanded(
            child: _selectedTabIndex == 0 ? _buildTasksTab() : _buildLogsTab(),
          ),
        ],
      ),
    );
  }

  Widget _buildTasksTab() {
    return FutureBuilder<PageData<TaskListItemModel>>(
      future: _tasksFuture,
      builder: (context, snapshot) {
        return LayoutBuilder(
          builder: (context, constraints) {
            final isCompact = constraints.maxWidth < 760;
            final viewportHeight = MediaQuery.sizeOf(context).height;
            final bodyHeight = (viewportHeight * 0.56).clamp(360.0, 620.0);
            final header = isCompact
                ? Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '任务管理',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 12,
                        runSpacing: 12,
                        children: [
                          FilledButton.icon(
                            onPressed: () => _openTaskEditor(),
                            icon: const Icon(Icons.add),
                            label: const Text('新建任务'),
                          ),
                          FilledButton.tonalIcon(
                            onPressed: _refresh,
                            icon: const Icon(Icons.refresh),
                            label: const Text('刷新'),
                          ),
                        ],
                      ),
                    ],
                  )
                : Row(
                    children: [
                      Text(
                        '任务管理',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      const Spacer(),
                      FilledButton.icon(
                        onPressed: () => _openTaskEditor(),
                        icon: const Icon(Icons.add),
                        label: const Text('新建任务'),
                      ),
                      const SizedBox(width: 12),
                      FilledButton.tonalIcon(
                        onPressed: _refresh,
                        icon: const Icon(Icons.refresh),
                        label: const Text('刷新'),
                      ),
                    ],
                  );

            final content = [
              header,
              const SizedBox(height: 12),
              Text(
                '创建采集任务、调整调度周期，并在需要时手动触发执行。',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              if (_listPollingTimer != null) ...[
                const SizedBox(height: 8),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFE8F0FE),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Text(
                    '最近有任务正在执行，列表会自动刷新。',
                  ),
                ),
              ],
              const SizedBox(height: 16),
              _TaskSummaryBar(
                  tasks: _applyFilters(snapshot.data?.items ?? const [])),
              const SizedBox(height: 16),
              _TaskFilterBar(
                searchController: _searchController,
                enabledFilter: _enabledFilter,
                resultFilter: _resultFilter,
                onSearchChanged: (value) {
                  setState(() {
                    _taskPage = 1;
                    _searchQuery = value.trim().toLowerCase();
                  });
                },
                onEnabledFilterChanged: (value) {
                  setState(() {
                    _taskPage = 1;
                    _enabledFilter = value;
                  });
                },
                onResultFilterChanged: (value) {
                  setState(() {
                    _taskPage = 1;
                    _resultFilter = value;
                  });
                },
                onClear: () {
                  _searchController.clear();
                  setState(() {
                    _taskPage = 1;
                    _searchQuery = '';
                    _enabledFilter = 'all';
                    _resultFilter = 'all';
                  });
                },
              ),
              const SizedBox(height: 16),
              SizedBox(
                height: bodyHeight,
                child: _buildBody(snapshot),
              ),
              const SizedBox(height: 12),
              _PaginationBar(
                page: snapshot.data?.page ?? _taskPage,
                pageSize: snapshot.data?.pageSize ?? _taskPageSize,
                total: snapshot.data?.total ?? 0,
                onPrevious: _taskPage > 1
                    ? () {
                        setState(() {
                          _taskPage -= 1;
                          _tasksFuture = _fetchTasks();
                        });
                      }
                    : null,
                onNext: ((snapshot.data?.page ?? _taskPage) *
                            (snapshot.data?.pageSize ?? _taskPageSize) <
                        (snapshot.data?.total ?? 0))
                    ? () {
                        setState(() {
                          _taskPage += 1;
                          _tasksFuture = _fetchTasks();
                        });
                      }
                    : null,
              ),
            ];

            return Scrollbar(
              thumbVisibility: true,
              child: ListView(
                padding: EdgeInsets.zero,
                children: content,
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildLogsTab() {
    return FutureBuilder<PageData<TaskLogItemModel>>(
      future: _logsFuture,
      builder: (context, snapshot) {
        final filteredLogs = _applyLogSearch(snapshot.data?.items ?? const []);
        return FutureBuilder<LogSummaryModel>(
          future: _logSummaryFuture,
          builder: (context, summarySnapshot) {
            final summary = summarySnapshot.data;
            return LayoutBuilder(
              builder: (context, constraints) {
                final isCompact = constraints.maxWidth < 760;
                final viewportHeight = MediaQuery.sizeOf(context).height;
                final bodyHeight = (viewportHeight * 0.56).clamp(360.0, 620.0);

                final header = isCompact
                    ? Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '全局日志',
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                          const SizedBox(height: 12),
                          FilledButton.tonalIcon(
                            onPressed: _refreshLogs,
                            icon: const Icon(Icons.refresh),
                            label: const Text('刷新'),
                          ),
                        ],
                      )
                    : Row(
                        children: [
                          Text(
                            '全局日志',
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                          const Spacer(),
                          FilledButton.tonalIcon(
                            onPressed: _refreshLogs,
                            icon: const Icon(Icons.refresh),
                            label: const Text('刷新'),
                          ),
                        ],
                      );

                final content = [
                  header,
                  const SizedBox(height: 12),
                  Text(
                    '查看全部任务的警告、错误与执行历史，快速定位异常。',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  const SizedBox(height: 16),
                  _LogSummaryBar(summary: summary),
                  const SizedBox(height: 16),
                  _FailedTaskActionBar(
                    logs: filteredLogs,
                    onOpenTask: _openTaskDetailsById,
                    onEditTask: _openTaskEditorById,
                    onRunTask: _runTaskById,
                  ),
                  const SizedBox(height: 16),
                  _LogFilterBar(
                    taskIdController: _logTaskIdController,
                    searchController: _logSearchController,
                    levelFilter: _logLevelFilter,
                    onLevelChanged: (value) {
                      setState(() {
                        _logPage = 1;
                        _logLevelFilter = value;
                      });
                      _refreshLogs();
                    },
                    onSearchChanged: (value) {
                      setState(() {
                        _logSearchQuery = value.trim().toLowerCase();
                      });
                    },
                    onApplyTaskId: () {
                      setState(() {
                        _logPage = 1;
                      });
                      return _refreshLogs();
                    },
                    onClear: () {
                      _logTaskIdController.clear();
                      _logSearchController.clear();
                      setState(() {
                        _logPage = 1;
                        _logLevelFilter = 'all';
                        _logSearchQuery = '';
                        _logsFuture = _fetchLogs();
                        _logSummaryFuture = _repository.fetchLogSummary();
                      });
                    },
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    height: bodyHeight,
                    child: _buildLogsBody(snapshot, filteredLogs),
                  ),
                  const SizedBox(height: 12),
                  _PaginationBar(
                    page: snapshot.data?.page ?? _logPage,
                    pageSize: snapshot.data?.pageSize ?? _logPageSize,
                    total: snapshot.data?.total ?? 0,
                    onPrevious: _logPage > 1
                        ? () {
                            setState(() {
                              _logPage -= 1;
                              _logsFuture = _fetchLogs();
                            });
                          }
                        : null,
                    onNext: ((snapshot.data?.page ?? _logPage) *
                                (snapshot.data?.pageSize ?? _logPageSize) <
                            (snapshot.data?.total ?? 0))
                        ? () {
                            setState(() {
                              _logPage += 1;
                              _logsFuture = _fetchLogs();
                            });
                          }
                        : null,
                  ),
                ];

                return Scrollbar(
                  thumbVisibility: true,
                  child: ListView(
                    padding: EdgeInsets.zero,
                    children: content,
                  ),
                );
              },
            );
          },
        );
      },
    );
  }

  Widget _buildBody(AsyncSnapshot<PageData<TaskListItemModel>> snapshot) {
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
              Text('正在刷新任务列表...'),
            ],
          ),
        ),
      );
    }

    if (snapshot.hasError) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Text('加载任务失败：${snapshot.error}'),
        ),
      );
    }

    final tasks =
        _applyFilters(snapshot.data?.items ?? const <TaskListItemModel>[]);
    if (tasks.isEmpty) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '暂无任务',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 8),
              const Text('先创建一个包含起始地址和定时表达式的采集任务。'),
              const SizedBox(height: 16),
              FilledButton.icon(
                onPressed: () => _openTaskEditor(),
                icon: const Icon(Icons.add),
                label: const Text('创建第一个任务'),
              ),
            ],
          ),
        ),
      );
    }

    return Card(
      child: Scrollbar(
        controller: _taskTableScrollController,
        thumbVisibility: true,
        trackVisibility: true,
        notificationPredicate: (notification) =>
            notification.metrics.axis == Axis.horizontal,
        child: SingleChildScrollView(
          controller: _taskTableScrollController,
          scrollDirection: Axis.horizontal,
          child: Padding(
            padding: const EdgeInsets.all(8),
            child: ConstrainedBox(
              constraints: const BoxConstraints(minWidth: 1180),
              child: DataTable(
                columnSpacing: 20,
                columns: const [
                  DataColumn(label: Text('名称')),
                  DataColumn(label: Text('地址')),
                  DataColumn(label: Text('定时')),
                  DataColumn(label: Text('状态')),
                  DataColumn(label: Text('最近运行')),
                  DataColumn(label: Text('最近结果')),
                  DataColumn(label: Text('创建时间')),
                  DataColumn(label: Text('操作')),
                ],
                rows: tasks.map(_buildTaskRow).toList(),
              ),
            ),
          ),
        ),
      ),
    );
  }

  DataRow _buildTaskRow(TaskListItemModel task) {
    return DataRow(
      cells: [
        DataCell(
          ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 180),
            child: Text(
              task.name,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ),
        DataCell(
          ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 320),
            child: Text(
              task.startUrl,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ),
        DataCell(Text(task.cronExpr)),
        DataCell(
          Chip(
            label: Text(task.isEnabled ? '已启用' : '已停用'),
            backgroundColor: task.isEnabled
                ? const Color(0xFFE3F6E8)
                : const Color(0xFFF3F4F6),
          ),
        ),
        DataCell(Text(_displayValue(task.lastRunAt))),
        DataCell(_TaskResultCell(task: task)),
        DataCell(Text(task.createdAt)),
        DataCell(
          SizedBox(
            width: 280,
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                FilledButton.tonalIcon(
                  style: FilledButton.styleFrom(
                    visualDensity: VisualDensity.compact,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 10,
                    ),
                    minimumSize: const Size(0, 36),
                    tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  ),
                  onPressed: () => _runTask(task),
                  icon: const Icon(Icons.play_arrow, size: 18),
                  label: const Text('运行'),
                ),
                const SizedBox(width: 8),
                OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    visualDensity: VisualDensity.compact,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 10,
                    ),
                    minimumSize: const Size(0, 36),
                    tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  ),
                  onPressed: () => _openTaskDetails(task),
                  icon: const Icon(Icons.info_outline, size: 18),
                  label: const Text('详情'),
                ),
                const SizedBox(width: 8),
                MenuAnchor(
                  menuChildren: [
                    MenuItemButton(
                      onPressed: () => _openTaskEditor(task),
                      child: const Text('编辑'),
                    ),
                    MenuItemButton(
                      onPressed: () => _saveTaskAsTemplate(task),
                      child: const Text('存为模板'),
                    ),
                    MenuItemButton(
                      onPressed: () => _toggleTask(task),
                      child: Text(task.isEnabled ? '停用' : '启用'),
                    ),
                    MenuItemButton(
                      onPressed: () => _deleteTask(task),
                      child: const Text('删除'),
                    ),
                  ],
                  builder: (context, controller, child) {
                    return OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        visualDensity: VisualDensity.compact,
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 10,
                        ),
                        minimumSize: const Size(0, 36),
                        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                      ),
                      onPressed: () {
                        if (controller.isOpen) {
                          controller.close();
                        } else {
                          controller.open();
                        }
                      },
                      icon: const Icon(Icons.more_horiz, size: 18),
                      label: const Text('更多'),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  List<TaskListItemModel> _applyFilters(List<TaskListItemModel> tasks) {
    return tasks.where((task) {
      final matchesSearch = _searchQuery.isEmpty ||
          task.name.toLowerCase().contains(_searchQuery) ||
          task.startUrl.toLowerCase().contains(_searchQuery) ||
          task.cronExpr.toLowerCase().contains(_searchQuery);

      final matchesEnabled = switch (_enabledFilter) {
        'enabled' => task.isEnabled,
        'disabled' => !task.isEnabled,
        _ => true,
      };

      final normalizedResult = task.lastRunStatus ?? 'never';
      final matchesResult = switch (_resultFilter) {
        'success' => normalizedResult == 'success',
        'failed' => normalizedResult == 'failed',
        'active' => _activeStatuses.contains(normalizedResult),
        'never' => normalizedResult == 'never',
        _ => true,
      };

      return matchesSearch && matchesEnabled && matchesResult;
    }).toList();
  }

  List<TaskLogItemModel> _applyLogSearch(List<TaskLogItemModel> logs) {
    if (_logSearchQuery.isEmpty) {
      return logs;
    }
    return logs.where((log) {
      return log.message.toLowerCase().contains(_logSearchQuery) ||
          (log.errorStack?.toLowerCase().contains(_logSearchQuery) ?? false) ||
          log.level.toLowerCase().contains(_logSearchQuery) ||
          log.createdAt.toLowerCase().contains(_logSearchQuery);
    }).toList();
  }

  Widget _buildLogsBody(
    AsyncSnapshot<PageData<TaskLogItemModel>> snapshot,
    List<TaskLogItemModel> logs,
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
              Text('正在刷新日志列表...'),
            ],
          ),
        ),
      );
    }

    if (snapshot.hasError) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Text('加载日志失败：${snapshot.error}'),
        ),
      );
    }

    if (logs.isEmpty) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Text(
            _logSearchQuery.isEmpty ? '当前筛选条件下没有日志。' : '当前搜索条件下没有日志。',
          ),
        ),
      );
    }

    return Card(
      child: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: logs.length,
        separatorBuilder: (_, __) => const Divider(height: 24),
        itemBuilder: (context, index) {
          final log = logs[index];
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _LogLevelBadge(level: log.level),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          log.message,
                          style: Theme.of(context).textTheme.titleSmall,
                        ),
                        const SizedBox(height: 6),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            _InlineMetaChip(label: '时间', value: log.createdAt),
                            _InlineMetaChip(
                              label: '任务 ID',
                              value: log.taskId?.toString() ?? '系统',
                            ),
                          ],
                        ),
                        if (log.taskId != null) ...[
                          const SizedBox(height: 10),
                          Wrap(
                            spacing: 8,
                            runSpacing: 8,
                            children: [
                              OutlinedButton(
                                onPressed: () =>
                                    _openTaskDetailsById(log.taskId!),
                                child: const Text('打开任务'),
                              ),
                              OutlinedButton(
                                onPressed: () =>
                                    _openTaskEditorById(log.taskId!),
                                child: const Text('编辑任务'),
                              ),
                              FilledButton.tonal(
                                onPressed: () => _runTaskById(log.taskId!),
                                child: const Text('重新运行'),
                              ),
                            ],
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
              if (log.errorStack != null && log.errorStack!.isNotEmpty) ...[
                const SizedBox(height: 10),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFE3E8EF)),
                  ),
                  child: SelectableText(
                    log.errorStack!,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ),
              ],
            ],
          );
        },
      ),
    );
  }
}

class _SystemManagementHero extends StatelessWidget {
  final Future<void> Function() onRefreshTasks;
  final Future<void> Function() onRefreshLogs;

  const _SystemManagementHero({
    required this.onRefreshTasks,
    required this.onRefreshLogs,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isCompact = constraints.maxWidth < 960;

        final infoColumn = Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '系统管理',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 8),
            Text(
              '统一管理采集任务、运行状态和平台日志，适合日常调度和故障排查。',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 16),
            const Wrap(
              spacing: 10,
              runSpacing: 10,
              children: [
                _SystemHeroChip(label: '任务调度'),
                _SystemHeroChip(label: '日志排障'),
                _SystemHeroChip(label: '模板协作'),
              ],
            ),
          ],
        );

        final actionColumn = Column(
          crossAxisAlignment:
              isCompact ? CrossAxisAlignment.start : CrossAxisAlignment.end,
          mainAxisSize: MainAxisSize.min,
          children: [
            FilledButton.tonalIcon(
              onPressed: onRefreshTasks,
              icon: const Icon(Icons.refresh),
              label: const Text('刷新任务'),
            ),
            const SizedBox(height: 10),
            FilledButton.tonalIcon(
              onPressed: onRefreshLogs,
              icon: const Icon(Icons.library_books_outlined),
              label: const Text('刷新日志'),
            ),
            const SizedBox(height: 12),
            const _SystemHeroChip(label: '下方切换任务 / 日志'),
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
                    infoColumn,
                    const SizedBox(height: 16),
                    actionColumn,
                  ],
                )
              : Row(
                  children: [
                    Expanded(child: infoColumn),
                    const SizedBox(width: 16),
                    actionColumn,
                  ],
                ),
        );
      },
    );
  }
}

class _SystemHeroChip extends StatelessWidget {
  final String label;

  const _SystemHeroChip({required this.label});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.16),
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: const Color(0x33FFFFFF)),
      ),
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.w700,
            ),
      ),
    );
  }
}

class _LogFilterBar extends StatelessWidget {
  final TextEditingController taskIdController;
  final TextEditingController searchController;
  final String levelFilter;
  final ValueChanged<String> onLevelChanged;
  final ValueChanged<String> onSearchChanged;
  final Future<void> Function() onApplyTaskId;
  final VoidCallback onClear;

  const _LogFilterBar({
    required this.taskIdController,
    required this.searchController,
    required this.levelFilter,
    required this.onLevelChanged,
    required this.onSearchChanged,
    required this.onApplyTaskId,
    required this.onClear,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Wrap(
          spacing: 12,
          runSpacing: 12,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            SizedBox(
              width: 180,
              child: TextField(
                controller: taskIdController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: '任务 ID',
                  hintText: '可选',
                ),
                onSubmitted: (_) => onApplyTaskId(),
              ),
            ),
            SizedBox(
              width: 180,
              child: DropdownButtonFormField<String>(
                initialValue: levelFilter,
                decoration: const InputDecoration(
                  labelText: '级别',
                ),
                items: const [
                  DropdownMenuItem(value: 'all', child: Text('全部')),
                  DropdownMenuItem(value: 'INFO', child: Text('INFO')),
                  DropdownMenuItem(value: 'WARNING', child: Text('WARNING')),
                  DropdownMenuItem(value: 'ERROR', child: Text('ERROR')),
                ],
                onChanged: (value) => onLevelChanged(value ?? 'all'),
              ),
            ),
            SizedBox(
              width: 320,
              child: TextField(
                controller: searchController,
                onChanged: onSearchChanged,
                decoration: const InputDecoration(
                  labelText: '搜索日志',
                  hintText: '消息、错误堆栈、级别、时间',
                  prefixIcon: Icon(Icons.search),
                ),
              ),
            ),
            FilledButton.tonal(
              onPressed: onApplyTaskId,
              child: const Text('应用'),
            ),
            OutlinedButton.icon(
              onPressed: onClear,
              icon: const Icon(Icons.clear),
              label: const Text('清空'),
            ),
          ],
        ),
      ),
    );
  }
}

class _InlineMetaChip extends StatelessWidget {
  final String label;
  final String value;

  const _InlineMetaChip({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: const Color(0xFFF3F6FA),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text('$label：$value'),
    );
  }
}

class _TaskFilterBar extends StatelessWidget {
  final TextEditingController searchController;
  final String enabledFilter;
  final String resultFilter;
  final ValueChanged<String> onSearchChanged;
  final ValueChanged<String> onEnabledFilterChanged;
  final ValueChanged<String> onResultFilterChanged;
  final VoidCallback onClear;

  const _TaskFilterBar({
    required this.searchController,
    required this.enabledFilter,
    required this.resultFilter,
    required this.onSearchChanged,
    required this.onEnabledFilterChanged,
    required this.onResultFilterChanged,
    required this.onClear,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Wrap(
          spacing: 12,
          runSpacing: 12,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            SizedBox(
              width: 280,
              child: TextField(
                controller: searchController,
                onChanged: onSearchChanged,
                decoration: const InputDecoration(
                  labelText: '搜索任务',
                  hintText: '名称、地址或定时表达式',
                  prefixIcon: Icon(Icons.search),
                ),
              ),
            ),
            SizedBox(
              width: 180,
              child: DropdownButtonFormField<String>(
                initialValue: enabledFilter,
                decoration: const InputDecoration(
                  labelText: '启用状态',
                ),
                items: const [
                  DropdownMenuItem(value: 'all', child: Text('全部')),
                  DropdownMenuItem(value: 'enabled', child: Text('已启用')),
                  DropdownMenuItem(value: 'disabled', child: Text('已停用')),
                ],
                onChanged: (value) => onEnabledFilterChanged(value ?? 'all'),
              ),
            ),
            SizedBox(
              width: 180,
              child: DropdownButtonFormField<String>(
                initialValue: resultFilter,
                decoration: const InputDecoration(
                  labelText: '最近结果',
                ),
                items: const [
                  DropdownMenuItem(value: 'all', child: Text('全部')),
                  DropdownMenuItem(value: 'active', child: Text('排队中 / 运行中')),
                  DropdownMenuItem(value: 'success', child: Text('成功')),
                  DropdownMenuItem(value: 'failed', child: Text('失败')),
                  DropdownMenuItem(value: 'never', child: Text('未运行')),
                ],
                onChanged: (value) => onResultFilterChanged(value ?? 'all'),
              ),
            ),
            OutlinedButton.icon(
              onPressed: onClear,
              icon: const Icon(Icons.clear),
              label: const Text('清空'),
            ),
          ],
        ),
      ),
    );
  }
}

class _TaskSummaryBar extends StatelessWidget {
  final List<TaskListItemModel> tasks;

  const _TaskSummaryBar({
    required this.tasks,
  });

  @override
  Widget build(BuildContext context) {
    final enabledCount = tasks.where((task) => task.isEnabled).length;
    final activeCount = tasks
        .where(
          (task) =>
              task.lastRunStatus == 'queued' || task.lastRunStatus == 'running',
        )
        .length;
    final failedCount =
        tasks.where((task) => task.lastRunStatus == 'failed').length;

    return Wrap(
      spacing: 16,
      runSpacing: 16,
      children: [
        _TaskMetricCard(
          title: '任务总数',
          value: '${tasks.length}',
          icon: Icons.assignment_outlined,
          accentColor: const Color(0xFF1E4F8A),
        ),
        _TaskMetricCard(
          title: '已启用',
          value: '$enabledCount',
          icon: Icons.toggle_on_outlined,
          accentColor: const Color(0xFF117A65),
        ),
        _TaskMetricCard(
          title: '排队中 / 运行中',
          value: '$activeCount',
          icon: Icons.timelapse_outlined,
          accentColor: const Color(0xFF2D6CDF),
        ),
        _TaskMetricCard(
          title: '最近失败',
          value: '$failedCount',
          icon: Icons.error_outline,
          accentColor: const Color(0xFFC45A1A),
        ),
      ],
    );
  }
}

class _TaskMetricCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color accentColor;

  const _TaskMetricCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.accentColor,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 190,
      child: Card(
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
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF2F6FC),
                        borderRadius: BorderRadius.circular(999),
                      ),
                      child: Text(
                        '实时',
                        style:
                            Theme.of(context).textTheme.labelMedium?.copyWith(
                                  color: accentColor,
                                  fontWeight: FontWeight.w700,
                                ),
                      ),
                    ),
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
      ),
    );
  }
}

class _TaskResultCell extends StatelessWidget {
  final TaskListItemModel task;

  const _TaskResultCell({
    required this.task,
  });

  @override
  Widget build(BuildContext context) {
    final status = task.lastRunStatus ?? 'never';
    final detail = task.lastErrorMessage;
    final color = switch (status) {
      'success' => const Color(0xFFE3F6E8),
      'failed' => const Color(0xFFFCE8E6),
      'queued' || 'running' => const Color(0xFFE8F0FE),
      _ => const Color(0xFFF3F4F6),
    };

    return Tooltip(
      message: detail == null || detail.isEmpty
          ? _statusLabel(status)
          : '${_statusLabel(status)}\n$detail',
      child: Chip(
        label: Text(_statusLabel(status)),
        backgroundColor: color,
      ),
    );
  }
}

String _statusLabel(String status) {
  return switch (status) {
    'success' => '成功',
    'failed' => '失败',
    'queued' => '排队中',
    'running' => '运行中',
    'never' => '未运行',
    _ => status,
  };
}

String _displayValue(String? value) {
  if (value == null || value.isEmpty) {
    return '-';
  }
  return value;
}

class _TaskEditorDialog extends StatefulWidget {
  final TaskListItemModel? task;
  final HttpTaskRepository repository;
  final TaskTemplateModel? initialTemplate;
  final List<TaskTemplateModel> templates;

  const _TaskEditorDialog({
    this.task,
    required this.repository,
    this.initialTemplate,
    required this.templates,
  });

  @override
  State<_TaskEditorDialog> createState() => _TaskEditorDialogState();
}

class _TaskEditorDialogState extends State<_TaskEditorDialog> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _nameController;
  late final TextEditingController _urlController;
  late final TextEditingController _cronController;
  late final TextEditingController _rulesController;
  late bool _enabled;
  bool _submitting = false;
  String? _submitError;

  @override
  void initState() {
    super.initState();
    final task = widget.task;
    _nameController = TextEditingController(text: task?.name ?? '');
    _urlController = TextEditingController(text: task?.startUrl ?? '');
    _cronController =
        TextEditingController(text: task?.cronExpr ?? '0 */6 * * *');
    _rulesController = TextEditingController(text: task?.parserRules ?? '');
    _enabled = task?.isEnabled ?? true;
    if (task == null && widget.initialTemplate != null) {
      _applyTemplate(widget.initialTemplate!);
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _urlController.dispose();
    _cronController.dispose();
    _rulesController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _submitting = true;
      _submitError = null;
    });

    final payload = TaskUpsertPayload(
      name: _nameController.text.trim(),
      startUrl: _urlController.text.trim(),
      parserRules: _nullableText(_rulesController.text),
      cronExpr: _cronController.text.trim(),
      status: _enabled ? 1 : 0,
    );

    try {
      if (widget.task == null) {
        await widget.repository.createTask(payload);
      } else {
        await widget.repository.updateTask(widget.task!.id, payload);
      }
      if (!mounted) {
        return;
      }
      Navigator.of(context).pop(true);
    } catch (error) {
      setState(() {
        _submitError = '$error';
      });
    } finally {
      if (mounted) {
        setState(() {
          _submitting = false;
        });
      }
    }
  }

  String? _nullableText(String value) {
    final trimmed = value.trim();
    if (trimmed.isEmpty) {
      return null;
    }
    return trimmed;
  }

  void _applyTemplate(TaskTemplateModel template) {
    setState(() {
      _nameController.text = template.name;
      _urlController.text = template.startUrl;
      _cronController.text = template.cronExpr;
      _rulesController.text = template.parserRules ?? '';
      _enabled = template.enabled;
      _submitError = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(widget.task == null ? '新建任务' : '编辑任务'),
      content: SizedBox(
        width: 520,
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (widget.task == null) ...[
                  Text(
                    '快捷模板',
                    style: Theme.of(context).textTheme.titleSmall,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '先选择一个模板预填常用采集配置，再按实际需求调整。',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: widget.templates.map((template) {
                      return ActionChip(
                        label: Text(template.label),
                        onPressed: () => _applyTemplate(template),
                      );
                    }).toList(),
                  ),
                  const SizedBox(height: 12),
                  ...widget.templates.map((template) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: Text(
                        '${template.label}: ${template.description}',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    );
                  }),
                  const SizedBox(height: 8),
                ],
                TextFormField(
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: '任务名称',
                  ),
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return '请输入任务名称。';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _urlController,
                  decoration: const InputDecoration(
                    labelText: '起始地址',
                  ),
                  validator: (value) {
                    final text = value?.trim() ?? '';
                    if (text.isEmpty) {
                      return '请输入起始地址。';
                    }
                    if (!text.startsWith('http://') &&
                        !text.startsWith('https://')) {
                      return '地址必须以 http:// 或 https:// 开头';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _cronController,
                  decoration: const InputDecoration(
                    labelText: '定时表达式',
                    helperText: '示例：0 */6 * * *',
                  ),
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return '请输入定时表达式。';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _rulesController,
                  maxLines: 5,
                  decoration: const InputDecoration(
                    labelText: '解析规则 JSON（可选）',
                  ),
                ),
                const SizedBox(height: 12),
                SwitchListTile(
                  contentPadding: EdgeInsets.zero,
                  title: const Text('立即启用任务'),
                  value: _enabled,
                  onChanged: (value) {
                    setState(() {
                      _enabled = value;
                    });
                  },
                ),
                if (_submitError != null) ...[
                  const SizedBox(height: 12),
                  Text(
                    _submitError!,
                    style: const TextStyle(color: Color(0xFFB3261E)),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed:
              _submitting ? null : () => Navigator.of(context).pop(false),
          child: const Text('取消'),
        ),
        FilledButton(
          onPressed: _submitting ? null : _submit,
          child: Text(_submitting ? '保存中...' : '保存'),
        ),
      ],
    );
  }
}

class _TaskDetailsDialog extends StatefulWidget {
  final TaskListItemModel task;
  final HttpTaskRepository repository;

  const _TaskDetailsDialog({
    required this.task,
    required this.repository,
  });

  @override
  State<_TaskDetailsDialog> createState() => _TaskDetailsDialogState();
}

class _TaskDetailsDialogState extends State<_TaskDetailsDialog> {
  static const _pollingStatuses = {'queued', 'running'};

  late Future<TaskListItemModel> _taskFuture;
  late Future<PageData<TaskLogItemModel>> _logsFuture;
  Timer? _pollingTimer;

  @override
  void initState() {
    super.initState();
    _taskFuture = widget.repository.fetchTask(widget.task.id);
    _logsFuture = widget.repository.fetchTaskLogs(widget.task.id);
    _maybeStartPolling(widget.task.lastRunStatus);
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    super.dispose();
  }

  Future<void> _refreshDetails() async {
    if (!mounted) {
      return;
    }

    final taskFuture = widget.repository.fetchTask(widget.task.id);
    final logsFuture = widget.repository.fetchTaskLogs(widget.task.id);

    setState(() {
      _taskFuture = taskFuture;
      _logsFuture = logsFuture;
    });

    try {
      final task = await taskFuture;
      _maybeStartPolling(task.lastRunStatus);
      if (!_shouldPoll(task.lastRunStatus)) {
        _pollingTimer?.cancel();
        _pollingTimer = null;
      }
    } catch (_) {
      _pollingTimer?.cancel();
      _pollingTimer = null;
    }
  }

  void _maybeStartPolling(String? status) {
    if (!_shouldPoll(status)) {
      _pollingTimer?.cancel();
      _pollingTimer = null;
      return;
    }

    _pollingTimer ??= Timer.periodic(
      const Duration(seconds: 3),
      (_) => _refreshDetails(),
    );
  }

  bool _shouldPoll(String? status) => _pollingStatuses.contains(status);

  Future<void> _refreshManually() async {
    await _refreshDetails();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Row(
        children: [
          Expanded(
            child: FutureBuilder<TaskListItemModel>(
              future: _taskFuture,
              initialData: widget.task,
              builder: (context, snapshot) {
                final task = snapshot.data ?? widget.task;
                return Text(
                  task.name,
                  overflow: TextOverflow.ellipsis,
                );
              },
            ),
          ),
          const SizedBox(width: 12),
          IconButton(
            tooltip: '刷新详情',
            onPressed: _refreshManually,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      content: SizedBox(
        width: 900,
        child: FutureBuilder<TaskListItemModel>(
          future: _taskFuture,
          initialData: widget.task,
          builder: (context, taskSnapshot) {
            if (taskSnapshot.connectionState == ConnectionState.waiting &&
                taskSnapshot.data == null) {
              return const Center(child: CircularProgressIndicator());
            }

            if (taskSnapshot.hasError && taskSnapshot.data == null) {
              return _DetailBlock(
                title: '任务加载失败',
                child: Text('加载任务详情失败：${taskSnapshot.error}'),
              );
            }

            final task = taskSnapshot.data ?? widget.task;
            final isPolling = _shouldPoll(task.lastRunStatus);

            return Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (isPolling)
                  Container(
                    width: double.infinity,
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFFE8F0FE),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      '该任务正在执行中，详情与日志会每 3 秒自动刷新一次。',
                    ),
                  ),
                Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  children: [
                    _DetailChip(label: '任务 ID', value: '${task.id}'),
                    _DetailChip(
                      label: '状态',
                      value: task.isEnabled ? '已启用' : '已停用',
                    ),
                    _DetailChip(
                      label: '最近运行',
                      value: _displayValue(task.lastRunAt),
                    ),
                    _DetailChip(
                      label: '最近成功',
                      value: _displayValue(task.lastSuccessAt),
                    ),
                    _DetailChip(
                      label: '最近结果',
                      value: _statusLabel(task.lastRunStatus ?? 'never'),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                _DetailBlock(
                  title: '起始地址',
                  child: SelectableText(task.startUrl),
                ),
                const SizedBox(height: 12),
                _DetailBlock(
                  title: '定时表达式',
                  child: Text(task.cronExpr),
                ),
                const SizedBox(height: 12),
                _DetailBlock(
                  title: '解析规则',
                  child: SelectableText(task.parserRules?.isNotEmpty == true
                      ? task.parserRules!
                      : '当前未配置解析规则。'),
                ),
                const SizedBox(height: 12),
                _DetailBlock(
                  title: '最近错误',
                  child: SelectableText(
                    task.lastErrorMessage?.isNotEmpty == true
                        ? task.lastErrorMessage!
                        : '最近没有错误信息。',
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  '最近日志',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                Flexible(
                  child: FutureBuilder<PageData<TaskLogItemModel>>(
                    future: _logsFuture,
                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.waiting) {
                        return const Center(child: CircularProgressIndicator());
                      }

                      if (snapshot.hasError) {
                        return _DetailBlock(
                          title: '日志加载失败',
                          child: Text('加载日志失败：${snapshot.error}'),
                        );
                      }

                      final logs =
                          snapshot.data?.items ?? const <TaskLogItemModel>[];
                      if (logs.isEmpty) {
                        return const _DetailBlock(
                          title: '日志',
                          child: Text('当前任务还没有可用日志。'),
                        );
                      }

                      return ListView.separated(
                        shrinkWrap: true,
                        itemCount: logs.length,
                        separatorBuilder: (_, __) => const Divider(height: 1),
                        itemBuilder: (context, index) {
                          final log = logs[index];
                          return ListTile(
                            contentPadding: EdgeInsets.zero,
                            leading: _LogLevelBadge(level: log.level),
                            title: Text(log.message),
                            subtitle: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const SizedBox(height: 4),
                                Text(log.createdAt),
                                if (log.errorStack != null &&
                                    log.errorStack!.isNotEmpty) ...[
                                  const SizedBox(height: 8),
                                  SelectableText(
                                    log.errorStack!,
                                    style:
                                        Theme.of(context).textTheme.bodySmall,
                                  ),
                                ],
                              ],
                            ),
                          );
                        },
                      );
                    },
                  ),
                ),
              ],
            );
          },
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

class _SaveTaskAsTemplateDialog extends StatefulWidget {
  final TaskListItemModel task;
  final HttpTemplateRepository repository;

  const _SaveTaskAsTemplateDialog({
    required this.task,
    required this.repository,
  });

  @override
  State<_SaveTaskAsTemplateDialog> createState() =>
      _SaveTaskAsTemplateDialogState();
}

class _SaveTaskAsTemplateDialogState extends State<_SaveTaskAsTemplateDialog> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _labelController;
  late final TextEditingController _descriptionController;
  late final TextEditingController _tagsController;
  bool _submitting = false;
  String? _submitError;

  @override
  void initState() {
    super.initState();
    _labelController = TextEditingController(
      text: '${widget.task.name} 模板',
    );
    _descriptionController = TextEditingController(
      text: '基于任务“${widget.task.name}”创建的模板。',
    );
    _tagsController = TextEditingController(text: '导入,任务');
  }

  @override
  void dispose() {
    _labelController.dispose();
    _descriptionController.dispose();
    _tagsController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _submitting = true;
      _submitError = null;
    });

    final template = TaskTemplateModel(
      id: _labelController.text.trim().toLowerCase().replaceAll(' ', '_'),
      label: _labelController.text.trim(),
      name: widget.task.name,
      startUrl: widget.task.startUrl,
      cronExpr: widget.task.cronExpr,
      parserRules: widget.task.parserRules,
      enabled: widget.task.isEnabled,
      description: _descriptionController.text.trim(),
      tags: _tagsController.text
          .split(',')
          .map((tag) => tag.trim())
          .where((tag) => tag.isNotEmpty)
          .toList(),
      usageCount: 0,
      lastUsedAt: null,
    );

    try {
      await widget.repository.createTaskTemplate(template);
      if (!mounted) {
        return;
      }
      Navigator.of(context).pop(true);
    } catch (error) {
      setState(() {
        _submitError = '$error';
      });
    } finally {
      if (mounted) {
        setState(() {
          _submitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('另存为模板'),
      content: SizedBox(
        width: 520,
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '将当前任务配置保存为可复用模板，便于后续快速建任务。',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _labelController,
                decoration: const InputDecoration(
                  labelText: '模板名称',
                ),
                validator: (value) =>
                    value == null || value.trim().isEmpty ? '必填项' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _descriptionController,
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: '模板说明',
                ),
                validator: (value) =>
                    value == null || value.trim().isEmpty ? '必填项' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _tagsController,
                decoration: const InputDecoration(
                  labelText: '标签',
                  hintText: '用英文逗号分隔多个标签',
                ),
              ),
              if (_submitError != null) ...[
                const SizedBox(height: 12),
                Text(
                  _submitError!,
                  style: const TextStyle(color: Color(0xFFB3261E)),
                ),
              ],
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed:
              _submitting ? null : () => Navigator.of(context).pop(false),
          child: const Text('取消'),
        ),
        FilledButton(
          onPressed: _submitting ? null : _submit,
          child: Text(_submitting ? '保存中...' : '保存模板'),
        ),
      ],
    );
  }
}

class _DetailChip extends StatelessWidget {
  final String label;
  final String value;

  const _DetailChip({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: const Color(0xFFF3F6FA),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label,
            style: Theme.of(context).textTheme.labelMedium,
          ),
          const SizedBox(height: 4),
          SelectableText(value),
        ],
      ),
    );
  }
}

class _DetailBlock extends StatelessWidget {
  final String title;
  final Widget child;

  const _DetailBlock({
    required this.title,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: const Color(0xFFE3E8EF)),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: Theme.of(context).textTheme.labelLarge,
          ),
          const SizedBox(height: 8),
          child,
        ],
      ),
    );
  }
}

class _LogLevelBadge extends StatelessWidget {
  final String level;

  const _LogLevelBadge({
    required this.level,
  });

  @override
  Widget build(BuildContext context) {
    final normalized = level.toUpperCase();
    final background = switch (normalized) {
      'ERROR' => const Color(0xFFFCE8E6),
      'WARNING' => const Color(0xFFFFF4E5),
      'INFO' => const Color(0xFFE8F0FE),
      _ => const Color(0xFFF3F4F6),
    };

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: background,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        normalized,
        style: Theme.of(context).textTheme.labelMedium,
      ),
    );
  }
}

class _PaginationBar extends StatelessWidget {
  final int page;
  final int pageSize;
  final int total;
  final VoidCallback? onPrevious;
  final VoidCallback? onNext;

  const _PaginationBar({
    required this.page,
    required this.pageSize,
    required this.total,
    required this.onPrevious,
    required this.onNext,
  });

  @override
  Widget build(BuildContext context) {
    final hasPrevious = onPrevious != null;
    final hasNext = onNext != null;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isCompact = constraints.maxWidth < 720;

            final info = Text(
              '第 $page 页 · 共 $total 条 · 每页 $pageSize 条',
              style: Theme.of(context).textTheme.bodyMedium,
            );

            final actions = Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                OutlinedButton.icon(
                  onPressed: hasPrevious ? onPrevious : null,
                  icon: const Icon(Icons.chevron_left),
                  label: const Text('上一页'),
                ),
                OutlinedButton.icon(
                  onPressed: hasNext ? onNext : null,
                  icon: const Icon(Icons.chevron_right),
                  label: const Text('下一页'),
                ),
              ],
            );

            if (isCompact) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  info,
                  const SizedBox(height: 12),
                  actions,
                ],
              );
            }

            return Row(
              children: [
                Expanded(child: info),
                const SizedBox(width: 16),
                actions,
              ],
            );
          },
        ),
      ),
    );
  }
}

class _LogSummaryBar extends StatelessWidget {
  final LogSummaryModel? summary;

  const _LogSummaryBar({required this.summary});

  @override
  Widget build(BuildContext context) {
    if (summary == null) {
      return const SizedBox.shrink();
    }

    return Wrap(
      spacing: 16,
      runSpacing: 16,
      children: [
        _TaskMetricCard(
          title: '日志总数',
          value: '${summary!.totalLogs}',
          icon: Icons.receipt_long_outlined,
          accentColor: const Color(0xFF1E4F8A),
        ),
        _TaskMetricCard(
          title: 'INFO',
          value: '${summary!.infoLogs}',
          icon: Icons.info_outline,
          accentColor: const Color(0xFF117A65),
        ),
        _TaskMetricCard(
          title: 'WARNING',
          value: '${summary!.warningLogs}',
          icon: Icons.warning_amber_outlined,
          accentColor: const Color(0xFFC45A1A),
        ),
        _TaskMetricCard(
          title: 'ERROR',
          value: '${summary!.errorLogs}',
          icon: Icons.error_outline,
          accentColor: const Color(0xFFB3261E),
        ),
      ],
    );
  }
}

class _FailedTaskActionBar extends StatelessWidget {
  final List<TaskLogItemModel> logs;
  final ValueChanged<int> onOpenTask;
  final ValueChanged<int> onEditTask;
  final ValueChanged<int> onRunTask;

  const _FailedTaskActionBar({
    required this.logs,
    required this.onOpenTask,
    required this.onEditTask,
    required this.onRunTask,
  });

  @override
  Widget build(BuildContext context) {
    final failedTaskIds = logs
        .where(
            (log) => log.taskId != null && log.level.toLowerCase() == 'error')
        .map((log) => log.taskId!)
        .toSet()
        .toList()
      ..sort();

    if (failedTaskIds.isEmpty) {
      return const SizedBox.shrink();
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '失败任务快捷操作',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: failedTaskIds.take(3).map((taskId) {
                return Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFE3E8EF)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        '任务 #$taskId',
                        style: Theme.of(context).textTheme.titleSmall,
                      ),
                      const SizedBox(height: 10),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          OutlinedButton(
                            onPressed: () => onOpenTask(taskId),
                            child: const Text('打开'),
                          ),
                          OutlinedButton(
                            onPressed: () => onEditTask(taskId),
                            child: const Text('编辑'),
                          ),
                          FilledButton.tonal(
                            onPressed: () => onRunTask(taskId),
                            child: const Text('重新运行'),
                          ),
                        ],
                      ),
                    ],
                  ),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
