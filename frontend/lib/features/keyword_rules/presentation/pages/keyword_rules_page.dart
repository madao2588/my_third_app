import 'package:flutter/material.dart';

import '../../../../core/utils/user_facing_error.dart';
import '../../../../core/widgets/async_error_panel.dart';
import '../../../../shared/models/page_data.dart';
import '../../data/models/keyword_rule_model.dart';
import '../../data/repositories/http_keyword_rule_repository.dart';

class KeywordRulesPage extends StatefulWidget {
  const KeywordRulesPage({super.key});

  @override
  State<KeywordRulesPage> createState() => _KeywordRulesPageState();
}

class _KeywordRulesPageState extends State<KeywordRulesPage> {
  late final HttpKeywordRuleRepository _repository;
  late Future<PageData<KeywordRuleModel>> _rulesFuture;

  @override
  void initState() {
    super.initState();
    _repository = HttpKeywordRuleRepository();
    _refresh();
  }

  void _refresh() {
    setState(() {
      _rulesFuture = _repository.getKeywordRules();
    });
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<PageData<KeywordRuleModel>>(
      future: _rulesFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 520),
              child: AsyncErrorPanel(
                error: snapshot.error!,
                title: '加载关键字规则失败',
                onRetry: _refresh,
              ),
            ),
          );
        }

        final rules = snapshot.data?.items ?? [];
        final total = snapshot.data?.total ?? 0;
        final enabledCount = rules.where((r) => r.isActive).length;
        final highPriorityCount = rules.where((r) => r.isHighPriority).length;

        final cards = [
          _RuleMetricCard(
            title: '规则总数',
            value: '$total',
            icon: Icons.rule_outlined,
            accentColor: const Color(0xFF1E4F8A),
          ),
          _RuleMetricCard(
            title: '已启用',
            value: '$enabledCount',
            icon: Icons.toggle_on_outlined,
            accentColor: const Color(0xFF117A65),
          ),
          _RuleMetricCard(
            title: '高优先级',
            value: '$highPriorityCount',
            icon: Icons.flag_outlined,
            accentColor: const Color(0xFFC45A1A),
          ),
        ];

        return Padding(
          padding: const EdgeInsets.all(24),
          child: LayoutBuilder(
            builder: (context, constraints) {
              final cardWidth = constraints.maxWidth >= 1200
                  ? (constraints.maxWidth - 32) / 3
                  : constraints.maxWidth >= 760
                      ? (constraints.maxWidth - 16) / 2
                      : constraints.maxWidth;

              return Scrollbar(
                thumbVisibility: true,
                child: ListView(
                  children: [
                    _KeywordRulesHero(
                        onCreateRule: () => _showRuleDialog(context)),
                    const SizedBox(height: 16),
                    Wrap(
                      spacing: 16,
                      runSpacing: 16,
                      children: cards
                          .map(
                              (card) => SizedBox(width: cardWidth, child: card))
                          .toList(),
                    ),
                    const SizedBox(height: 16),
                    _SectionCard(
                      title: '关键字规则列表',
                      child: Container(
                        width: double.infinity,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                              color: Colors.grey.withValues(alpha: 0.2)),
                        ),
                        child: SingleChildScrollView(
                          scrollDirection: Axis.horizontal,
                          child: DataTable(
                            columns: const [
                              DataColumn(label: Text('关键词')),
                              DataColumn(label: Text('高优标注')),
                              DataColumn(label: Text('启用状态')),
                              DataColumn(label: Text('操作')),
                            ],
                            rows: rules.map((r) {
                              return DataRow(cells: [
                                DataCell(
                                  Text(
                                    r.word,
                                    style: const TextStyle(
                                      fontWeight: FontWeight.bold,
                                      color: Color(0xFF1E4F8A),
                                    ),
                                  ),
                                ),
                                DataCell(
                                  Switch(
                                    value: r.isHighPriority,
                                    onChanged: (v) =>
                                        _toggleHighPriority(context, r, v),
                                  ),
                                ),
                                DataCell(
                                  Switch(
                                    value: r.isActive,
                                    activeThumbColor: const Color(0xFF117A65),
                                    onChanged: (v) => _toggleActive(context, r),
                                  ),
                                ),
                                DataCell(
                                  Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      IconButton(
                                        icon: const Icon(Icons.edit_outlined,
                                            size: 20),
                                        tooltip: '编辑',
                                        onPressed: () =>
                                            _showRuleDialog(context, rule: r),
                                      ),
                                      IconButton(
                                        icon: const Icon(Icons.delete_outline,
                                            size: 20, color: Colors.red),
                                        tooltip: '删除',
                                        onPressed: () =>
                                            _deleteRule(context, r),
                                      ),
                                    ],
                                  ),
                                ),
                              ]);
                            }).toList(),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        );
      },
    );
  }

  void _showRuleDialog(BuildContext context, {KeywordRuleModel? rule}) {
    showDialog(
      context: context,
      builder: (context) {
        String word = rule?.word ?? '';
        bool isHighPriority = rule?.isHighPriority ?? false;
        bool isActive = rule?.isActive ?? true;

        return StatefulBuilder(
          builder: (context, setDialogState) {
            return AlertDialog(
              title: Text(rule == null ? '新建关键字' : '编辑关键字'),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextField(
                    decoration: const InputDecoration(labelText: '关键词'),
                    controller: TextEditingController(text: word)
                      ..selection =
                          TextSelection.collapsed(offset: word.length),
                    onChanged: (v) => word = v,
                  ),
                  const SizedBox(height: 16),
                  SwitchListTile(
                    title: const Text('高优标注'),
                    value: isHighPriority,
                    onChanged: (v) => setDialogState(() => isHighPriority = v),
                  ),
                  SwitchListTile(
                    title: const Text('启用状态'),
                    value: isActive,
                    onChanged: (v) => setDialogState(() => isActive = v),
                  ),
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('取消'),
                ),
                FilledButton(
                  onPressed: () async {
                    if (word.trim().isEmpty) return;
                    Navigator.pop(context);
                    final newRule = KeywordRuleModel(
                      id: rule?.id ?? 0,
                      word: word.trim(),
                      isHighPriority: isHighPriority,
                      isActive: isActive,
                      createdAt: '',
                      updatedAt: '',
                    );

                    try {
                      if (rule == null) {
                        await _repository.createKeywordRule(newRule);
                      } else {
                        await _repository.updateKeywordRule(newRule);
                      }
                      _refresh();
                    } catch (e) {
                      if (!context.mounted) return;
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('保存失败：${userFacingError(e)}'),
                        ),
                      );
                    }
                  },
                  child: const Text('保存'),
                ),
              ],
            );
          },
        );
      },
    );
  }

  Future<void> _toggleHighPriority(
      BuildContext context, KeywordRuleModel rule, bool newValue) async {
    try {
      final updated = KeywordRuleModel(
        id: rule.id,
        word: rule.word,
        isHighPriority: newValue,
        isActive: rule.isActive,
        createdAt: '',
        updatedAt: '',
      );
      await _repository.updateKeywordRule(updated);
      _refresh();
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('更新失败：${userFacingError(e)}')),
      );
    }
  }

  Future<void> _toggleActive(
      BuildContext context, KeywordRuleModel rule) async {
    try {
      await _repository.toggleKeywordRuleActive(rule.id);
      _refresh();
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('操作失败：${userFacingError(e)}')),
      );
    }
  }

  Future<void> _deleteRule(BuildContext context, KeywordRuleModel rule) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('确认删除'),
        content: Text('确定要删除关键字 "${rule.word}" 吗？此操作不可恢复。'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: const Text('取消')),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('删除'),
          ),
        ],
      ),
    );
    if (confirm != true) return;

    try {
      await _repository.deleteKeywordRule(rule.id);
      _refresh();
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('删除失败：${userFacingError(e)}')),
      );
    }
  }
}

class _KeywordRulesHero extends StatelessWidget {
  final VoidCallback? onCreateRule;

  const _KeywordRulesHero({required this.onCreateRule});

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
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF1D4E89).withValues(alpha: 0.15),
            blurRadius: 30,
            offset: const Offset(0, 16),
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
                  '关键词规则',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: Colors.white,
                      ),
                ),
                const SizedBox(height: 10),
                Text(
                  '支持动态配置监控的高优先级关键词及启用状态，更新后即刻生效。',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: const Color(0xE6F3F8FF),
                      ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 16),
          FilledButton.tonalIcon(
            onPressed: onCreateRule,
            icon: const Icon(Icons.add),
            label: const Text('新建规则'),
          ),
        ],
      ),
    );
  }
}

class _RuleMetricCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color accentColor;

  const _RuleMetricCard({
    required this.title,
    required this.value,
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
              accentColor.withValues(alpha: 0.05),
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
              const SizedBox(height: 14),
              Text(title, style: Theme.of(context).textTheme.titleMedium),
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

class _SectionCard extends StatelessWidget {
  final String title;
  final Widget child;

  const _SectionCard({required this.title, required this.child});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 16),
            child,
          ],
        ),
      ),
    );
  }
}
