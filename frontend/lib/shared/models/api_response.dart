class ApiResponse<T> {
  final int code;
  final String message;
  final T? data;

  const ApiResponse({
    required this.code,
    required this.message,
    required this.data,
  });

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object? rawData) fromData,
  ) {
    return ApiResponse<T>(
      code: json['code'] as int? ?? -1,
      message: json['message']?.toString() ?? 'unknown',
      data: fromData(json['data']),
    );
  }
}
