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

  ApiClient({
    String? baseUrl,
    http.Client? httpClient,
  })  : baseUrl = baseUrl ?? AppConfig.apiBaseUrl,
        _httpClient = httpClient ?? http.Client();

  Future<Map<String, dynamic>> getJson(
    String path, {
    Map<String, String>? queryParameters,
  }) async {
    final uri = Uri.parse('$baseUrl$path').replace(
      queryParameters: queryParameters,
    );
    final response = await _httpClient.get(uri, headers: _headers());
    return _decodeResponse(response);
  }

  Future<Map<String, dynamic>> postJson(
    String path, {
    Map<String, dynamic>? body,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    final response = await _httpClient.post(
      uri,
      headers: _headers(includeContentType: true),
      body: body == null ? null : jsonEncode(body),
    );
    return _decodeResponse(response);
  }

  Future<Map<String, dynamic>> putJson(
    String path, {
    Map<String, dynamic>? body,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    final response = await _httpClient.put(
      uri,
      headers: _headers(includeContentType: true),
      body: body == null ? null : jsonEncode(body),
    );
    return _decodeResponse(response);
  }

  Future<Map<String, dynamic>> deleteJson(String path) async {
    final uri = Uri.parse('$baseUrl$path');
    final response = await _httpClient.delete(uri, headers: _headers());
    return _decodeResponse(response);
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
    final decoded = jsonDecode(response.body);
    if (decoded is! Map<String, dynamic>) {
      throw const ApiException('Invalid API response format');
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
