import 'package:flutter/material.dart';

import '../../../system_management/data/models/task_template_models.dart';
import '../../../system_management/data/repositories/http_template_repository.dart';

class SourceSitesPage extends StatefulWidget {
  final ValueChanged<TaskTemplateModel>? onUseTemplate;
  final List<TaskTemplateModel> templates;
  final HttpTemplateRepository templateRepository;
  final Future<void> Function() onTemplatesChanged;

  const SourceSitesPage({
    super.key,
    this.onUseTemplate,
    required this.templates,
    required this.templateRepository,
    required this.onTemplatesChanged,
  });

  @override
  State<SourceSitesPage> createState() => _SourceSitesPageState();
}

class _SourceSitesPageState extends State<SourceSitesPage> {
  Future<void> _useTemplate(TaskTemplateModel template) async {
    try {
      await widget.templateRepository.trackTaskTemplateUse(template.id);
      await widget.onTemplatesChanged();
      widget.onUseTemplate?.call(template);
    } catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('套用模板失败：$error'),
          backgroundColor: const Color(0xFFB3261E),
        ),
      );
    }
  }

  Future<void> _openTemplateEditor([TaskTemplateModel? template]) async {
    final saved = await showDialog<bool>(
      context: context,
      builder: (context) => _TemplateEditorDialog(
        template: template,
        repository: widget.templateRepository,
      ),
    );

    if (saved == true && mounted) {
      await widget.onTemplatesChanged();
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(template == null ? '模板已创建。' : '模板已更新。'),
        ),
      );
    }
  }

  Future<void> _deleteTemplate(TaskTemplateModel template) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('删除模板？'),
        content: Text('这会永久删除“${template.label}”。'),
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
      await widget.templateRepository.deleteTaskTemplate(template.id);
      await widget.onTemplatesChanged();
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('模板“${template.label}”已删除。')),
      );
    } catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('删除模板失败：$error'),
          backgroundColor: const Color(0xFFB3261E),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _SourceSitesHero(
            templates: widget.templates,
            onCreate: () => _openTemplateEditor(),
          ),
          const SizedBox(height: 16),
          Expanded(
            child: widget.templates.isEmpty
                ? _SourceSitesEmptyState(
                    onCreate: () => _openTemplateEditor(),
                  )
                : Scrollbar(
                    thumbVisibility: true,
                    child: ListView.separated(
                      itemCount: widget.templates.length,
                      separatorBuilder: (_, __) => const SizedBox(height: 16),
                      itemBuilder: (context, index) {
                        final template = widget.templates[index];
                        return Card(
                          child: Container(
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                                colors: [
                                  const Color(0xFF1E4F8A)
                                      .withValues(alpha: 0.05),
                                  Colors.white,
                                ],
                              ),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(20),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Expanded(
                                        child: Text(
                                          template.label,
                                          style: Theme.of(context)
                                              .textTheme
                                              .titleLarge,
                                        ),
                                      ),
                                      Wrap(
                                        spacing: 8,
                                        runSpacing: 8,
                                        children: template.tags
                                            .map(
                                                (tag) => Chip(label: Text(tag)))
                                            .toList(),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 12),
                                  Text(
                                    template.description,
                                    style:
                                        Theme.of(context).textTheme.bodyMedium,
                                  ),
                                  const SizedBox(height: 16),
                                  _TemplateMetaRow(
                                    label: '建议任务名',
                                    value: template.name,
                                  ),
                                  _TemplateMetaRow(
                                    label: '起始地址',
                                    value: template.startUrl,
                                  ),
                                  _TemplateMetaRow(
                                    label: '定时表达式',
                                    value: template.cronExpr,
                                  ),
                                  _TemplateMetaRow(
                                    label: '解析规则',
                                    value: template.parserRules ?? '使用可读性兜底解析',
                                  ),
                                  _TemplateMetaRow(
                                    label: '使用情况',
                                    value: '已使用 ${template.usageCount} 次'
                                        '${template.lastUsedAt == null ? '' : ' · 最近使用 ${template.lastUsedAt}'}',
                                  ),
                                  const SizedBox(height: 8),
                                  Wrap(
                                    spacing: 8,
                                    runSpacing: 8,
                                    children: [
                                      FilledButton.tonal(
                                        onPressed: widget.onUseTemplate == null
                                            ? null
                                            : () => _useTemplate(template),
                                        child: const Text('使用此模板'),
                                      ),
                                      OutlinedButton(
                                        onPressed: () =>
                                            _openTemplateEditor(template),
                                        child: const Text('编辑'),
                                      ),
                                      OutlinedButton(
                                        onPressed: () =>
                                            _deleteTemplate(template),
                                        style: OutlinedButton.styleFrom(
                                          foregroundColor:
                                              const Color(0xFFB3261E),
                                        ),
                                        child: const Text('删除'),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}

class _SourceSitesHero extends StatelessWidget {
  final List<TaskTemplateModel> templates;
  final VoidCallback onCreate;

  const _SourceSitesHero({
    required this.templates,
    required this.onCreate,
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
              '来源站点模板',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    color: Colors.white,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              '为常见来源站点沉淀可复用的采集模板，减少重复配置工作。',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: const Color(0xE6F3F8FF),
                  ),
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 10,
              runSpacing: 10,
              children: [
                _HeroChip(label: '模板总数 ${templates.length}'),
                const _HeroChip(label: '一键套用任务蓝图'),
                const _HeroChip(label: '支持 CRUD 与使用统计'),
              ],
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
                    FilledButton.icon(
                      onPressed: onCreate,
                      icon: const Icon(Icons.add),
                      label: const Text('新建模板'),
                    ),
                  ],
                )
              : Row(
                  children: [
                    Expanded(child: content),
                    const SizedBox(width: 16),
                    FilledButton.icon(
                      onPressed: onCreate,
                      icon: const Icon(Icons.add),
                      label: const Text('新建模板'),
                    ),
                  ],
                ),
        );
      },
    );
  }
}

class _SourceSitesEmptyState extends StatelessWidget {
  final VoidCallback onCreate;

  const _SourceSitesEmptyState({required this.onCreate});

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
              child:
                  const Icon(Icons.language_outlined, color: Color(0xFF1E4F8A)),
            ),
            const SizedBox(height: 18),
            Text('还没有模板', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 10),
            Text(
              '先创建一个模板，再通过模板快速生成任务并沉淀来源站点配置。',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 18),
            FilledButton.icon(
              onPressed: onCreate,
              icon: const Icon(Icons.add),
              label: const Text('创建第一个模板'),
            ),
          ],
        ),
      ),
    );
  }
}

class _HeroChip extends StatelessWidget {
  final String label;

  const _HeroChip({required this.label});

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

class _TemplateMetaRow extends StatelessWidget {
  final String label;
  final String value;

  const _TemplateMetaRow({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: Theme.of(context).textTheme.labelLarge,
          ),
          const SizedBox(height: 4),
          SelectableText(value),
        ],
      ),
    );
  }
}

class _TemplateEditorDialog extends StatefulWidget {
  final TaskTemplateModel? template;
  final HttpTemplateRepository repository;

  const _TemplateEditorDialog({
    this.template,
    required this.repository,
  });

  @override
  State<_TemplateEditorDialog> createState() => _TemplateEditorDialogState();
}

class _TemplateEditorDialogState extends State<_TemplateEditorDialog> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _labelController;
  late final TextEditingController _nameController;
  late final TextEditingController _urlController;
  late final TextEditingController _cronController;
  late final TextEditingController _rulesController;
  late final TextEditingController _descriptionController;
  late final TextEditingController _tagsController;
  late bool _enabled;
  bool _submitting = false;
  String? _submitError;

  @override
  void initState() {
    super.initState();
    final template = widget.template;
    _labelController = TextEditingController(text: template?.label ?? '');
    _nameController = TextEditingController(text: template?.name ?? '');
    _urlController = TextEditingController(text: template?.startUrl ?? '');
    _cronController =
        TextEditingController(text: template?.cronExpr ?? '0 */6 * * *');
    _rulesController = TextEditingController(text: template?.parserRules ?? '');
    _descriptionController =
        TextEditingController(text: template?.description ?? '');
    _tagsController =
        TextEditingController(text: template?.tags.join(', ') ?? '');
    _enabled = template?.enabled ?? true;
  }

  @override
  void dispose() {
    _labelController.dispose();
    _nameController.dispose();
    _urlController.dispose();
    _cronController.dispose();
    _rulesController.dispose();
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
      id: widget.template?.id ??
          _labelController.text.trim().toLowerCase().replaceAll(' ', '_'),
      label: _labelController.text.trim(),
      name: _nameController.text.trim(),
      startUrl: _urlController.text.trim(),
      cronExpr: _cronController.text.trim(),
      parserRules: _nullableText(_rulesController.text),
      enabled: _enabled,
      description: _descriptionController.text.trim(),
      tags: _tagsController.text
          .split(',')
          .map((tag) => tag.trim())
          .where((tag) => tag.isNotEmpty)
          .toList(),
      usageCount: widget.template?.usageCount ?? 0,
      lastUsedAt: widget.template?.lastUsedAt,
    );

    try {
      if (widget.template == null) {
        await widget.repository.createTaskTemplate(template);
      } else {
        await widget.repository.updateTaskTemplate(template);
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

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(widget.template == null ? '新建模板' : '编辑模板'),
      content: SizedBox(
        width: 560,
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
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
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: '建议任务名',
                  ),
                  validator: (value) =>
                      value == null || value.trim().isEmpty ? '必填项' : null,
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
                      return '必填项';
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
                  ),
                  validator: (value) =>
                      value == null || value.trim().isEmpty ? '必填项' : null,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _rulesController,
                  maxLines: 4,
                  decoration: const InputDecoration(
                    labelText: '解析规则 JSON',
                  ),
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
                const SizedBox(height: 12),
                SwitchListTile(
                  contentPadding: EdgeInsets.zero,
                  title: const Text('默认启用'),
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
