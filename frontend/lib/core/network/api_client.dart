import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/app_config.dart';

class ApiClient {
  static String? _authToken;

  static void setAuthToken(String? token) {
    _authToken = token;
  }

  final String baseUrl;
  final http.Client _httpClient;
  final Duration requestTimeout;

  ApiClient({
    String? baseUrl,
    http.Client? httpClient,
    Duration? requestTimeout,
  })  : baseUrl = baseUrl ?? AppConfig.apiBaseUrl,
        _httpClient = httpClient ?? http.Client(),
        requestTimeout = requestTimeout ?? AppConfig.apiRequestTimeout;

  Future<List<int>> getBytes(
    String path, {
    Map<String, String>? queryParameters,
  }) async {
    final uri = Uri.parse('$baseUrl$path').replace(
      queryParameters: queryParameters,
    );
    final response = await _httpClient
        .get(uri, headers: _headers())
        .timeout(requestTimeout, onTimeout: _onTimeout);
    if (response.statusCode < 200 || response.statusCode >= 300) {
      var msg = 'Request failed (${response.statusCode})';
      try {
        final decoded = jsonDecode(response.body);
        if (decoded is Map && decoded['message'] != null) {
          msg = decoded['message'].toString();
        }
      } on FormatException {
        if (response.body.isNotEmpty && response.body.length < 240) {
          msg = response.body;
        }
      } catch (_) {
        if (response.body.isNotEmpty && response.body.length < 240) {
          msg = response.body;
        }
      }
      throw ApiException(msg, statusCode: response.statusCode);
    }
    return response.bodyBytes;
  }

  Future<Map<String, dynamic>> getJson(
    String path, {
    Map<String, String>? queryParameters,
  }) async {
    final uri = Uri.parse('$baseUrl$path').replace(
      queryParameters: queryParameters,
    );
    final response = await _httpClient
        .get(uri, headers: _headers())
        .timeout(requestTimeout, onTimeout: _onTimeout);
    return _decodeResponse(response);
  }

  Future<Map<String, dynamic>> postJson(
    String path, {
    Map<String, dynamic>? body,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    final response = await _httpClient
        .post(
          uri,
          headers: _headers(includeContentType: true),
          body: body == null ? null : jsonEncode(body),
        )
        .timeout(requestTimeout, onTimeout: _onTimeout);
    return _decodeResponse(response);
  }

  Future<Map<String, dynamic>> putJson(
    String path, {
    Map<String, dynamic>? body,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    final response = await _httpClient
        .put(
          uri,
          headers: _headers(includeContentType: true),
          body: body == null ? null : jsonEncode(body),
        )
        .timeout(requestTimeout, onTimeout: _onTimeout);
    return _decodeResponse(response);
  }

  Future<Map<String, dynamic>> deleteJson(String path) async {
    final uri = Uri.parse('$baseUrl$path');
    final response = await _httpClient
        .delete(uri, headers: _headers())
        .timeout(requestTimeout, onTimeout: _onTimeout);
    return _decodeResponse(response);
  }

  Never _onTimeout() {
    throw const ApiException('Request timed out');
  }

  Map<String, String> _headers({bool includeContentType = false}) {
    final headers = <String, String>{};
    if (includeContentType) {
      headers['Content-Type'] = 'application/json';
    }
    final token = _authToken;
    if (token != null && token.isNotEmpty) {
      headers['Authorization'] = 'Bearer $token';
    }
    return headers;
  }

  Map<String, dynamic> _decodeResponse(http.Response response) {
    late final Map<String, dynamic> decoded;
    try {
      final raw = jsonDecode(response.body);
      if (raw is! Map<String, dynamic>) {
        throw ApiException('服务器返回格式异常', statusCode: response.statusCode);
      }
      decoded = raw;
    } on FormatException {
      throw ApiException('服务器返回了无法解析的 JSON', statusCode: response.statusCode);
    }

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw ApiException(
        decoded['message']?.toString() ?? 'Request failed',
        statusCode: response.statusCode,
      );
    }

    return decoded;
  }

  void dispose() {
    _httpClient.close();
  }
}

class ApiException implements Exception {
  final String message;
  final int? statusCode;

  const ApiException(
    this.message, {
    this.statusCode,
  });

  @override
  String toString() {
    if (statusCode == null) {
      return 'ApiException($message)';
    }
    return 'ApiException($statusCode, $message)';
  }
}
