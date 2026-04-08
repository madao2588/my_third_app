class TaskTemplateModel {
  final String id;
  final String label;
  final String name;
  final String startUrl;
  final String cronExpr;
  final String? parserRules;
  final bool enabled;
  final String description;
  final List<String> tags;
  final int usageCount;
  final String? lastUsedAt;

  const TaskTemplateModel({
    required this.id,
    required this.label,
    required this.name,
    required this.startUrl,
    required this.cronExpr,
    required this.parserRules,
    required this.enabled,
    required this.description,
    required this.tags,
    required this.usageCount,
    required this.lastUsedAt,
  });

  factory TaskTemplateModel.fromJson(Map<String, dynamic> json) {
    return TaskTemplateModel(
      id: json['id']?.toString() ?? '',
      label: json['label']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      startUrl: json['start_url']?.toString() ?? '',
      cronExpr: json['cron_expr']?.toString() ?? '',
      parserRules: json['parser_rules']?.toString(),
      enabled: json['enabled'] as bool? ?? true,
      description: json['description']?.toString() ?? '',
      tags: (json['tags'] as List<dynamic>? ?? [])
          .map((item) => item.toString())
          .toList(),
      usageCount: json['usage_count'] as int? ?? 0,
      lastUsedAt: json['last_used_at']?.toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'label': label,
      'name': name,
      'start_url': startUrl,
      'cron_expr': cronExpr,
      'parser_rules': parserRules,
      'enabled': enabled,
      'description': description,
      'tags': tags,
      'usage_count': usageCount,
      'last_used_at': lastUsedAt,
    };
  }
}
