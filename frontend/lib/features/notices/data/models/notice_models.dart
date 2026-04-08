class NoticeListItemModel {
  final int id;
  final String title;
  final String summary;
  final String sourceSite;
  final String sourceUrl;
  final String? publishedAt;
  final String capturedAt;
  final int qualityScore;
  final List<String> matchedKeywords;
  final bool isHighPriority;
  final int taskId;

  const NoticeListItemModel({
    required this.id,
    required this.title,
    required this.summary,
    required this.sourceSite,
    required this.sourceUrl,
    required this.publishedAt,
    required this.capturedAt,
    required this.qualityScore,
    required this.matchedKeywords,
    required this.isHighPriority,
    required this.taskId,
  });

  factory NoticeListItemModel.fromJson(Map<String, dynamic> json) {
    return NoticeListItemModel(
      id: json['id'] as int? ?? 0,
      title: json['title']?.toString() ?? '',
      summary: json['summary']?.toString() ?? '',
      sourceSite: json['source_site']?.toString() ?? '',
      sourceUrl: json['source_url']?.toString() ?? '',
      publishedAt: json['published_at']?.toString(),
      capturedAt: json['captured_at']?.toString() ?? '',
      qualityScore: json['quality_score'] as int? ?? 0,
      matchedKeywords: (json['matched_keywords'] as List<dynamic>? ?? [])
          .map((item) => item.toString())
          .toList(),
      isHighPriority: json['is_high_priority'] as bool? ?? false,
      taskId: json['task_id'] as int? ?? 0,
    );
  }
}

class NoticeDetailModel extends NoticeListItemModel {
  final String contentText;
  final String contentHtml;
  final String? contentHash;
  final String? snapshotPath;

  const NoticeDetailModel({
    required super.id,
    required super.title,
    required super.summary,
    required super.sourceSite,
    required super.sourceUrl,
    required super.publishedAt,
    required super.capturedAt,
    required super.qualityScore,
    required super.matchedKeywords,
    required super.isHighPriority,
    required super.taskId,
    required this.contentText,
    required this.contentHtml,
    required this.contentHash,
    required this.snapshotPath,
  });

  factory NoticeDetailModel.fromJson(Map<String, dynamic> json) {
    return NoticeDetailModel(
      id: json['id'] as int? ?? 0,
      title: json['title']?.toString() ?? '',
      summary: json['summary']?.toString() ?? '',
      sourceSite: json['source_site']?.toString() ?? '',
      sourceUrl: json['source_url']?.toString() ?? '',
      publishedAt: json['published_at']?.toString(),
      capturedAt: json['captured_at']?.toString() ?? '',
      qualityScore: json['quality_score'] as int? ?? 0,
      matchedKeywords: (json['matched_keywords'] as List<dynamic>? ?? [])
          .map((item) => item.toString())
          .toList(),
      isHighPriority: json['is_high_priority'] as bool? ?? false,
      taskId: json['task_id'] as int? ?? 0,
      contentText: json['content_text']?.toString() ?? '',
      contentHtml: json['content_html']?.toString() ?? '',
      contentHash: json['content_hash']?.toString(),
      snapshotPath: json['snapshot_path']?.toString(),
    );
  }
}

class NoticeSnapshotModel {
  final int id;
  final String sourceUrl;
  final String sourceSite;
  final String snapshotPath;
  final String content;

  const NoticeSnapshotModel({
    required this.id,
    required this.sourceUrl,
    required this.sourceSite,
    required this.snapshotPath,
    required this.content,
  });

  factory NoticeSnapshotModel.fromJson(Map<String, dynamic> json) {
    return NoticeSnapshotModel(
      id: json['id'] as int? ?? 0,
      sourceUrl: json['source_url']?.toString() ?? '',
      sourceSite: json['source_site']?.toString() ?? '',
      snapshotPath: json['snapshot_path']?.toString() ?? '',
      content: json['content']?.toString() ?? '',
    );
  }
}
