class PageData<T> {
  final List<T> items;
  final int total;
  final int page;
  final int pageSize;

  const PageData({
    required this.items,
    required this.total,
    required this.page,
    required this.pageSize,
  });

  factory PageData.fromJson(
    Map<String, dynamic> json,
    T Function(Map<String, dynamic> item) fromItem,
  ) {
    final rawItems = (json['items'] as List<dynamic>? ?? [])
        .whereType<Map<String, dynamic>>()
        .map(fromItem)
        .toList();

    return PageData<T>(
      items: rawItems,
      total: json['total'] as int? ?? 0,
      page: json['page'] as int? ?? 1,
      pageSize: json['page_size'] as int? ?? 20,
    );
  }
}
