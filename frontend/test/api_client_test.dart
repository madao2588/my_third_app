import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:pharma_bid_monitor_frontend/core/network/api_client.dart';

void main() {
  tearDown(() {
    ApiClient.setAuthToken(null);
  });

  test('getJson returns decoded envelope', () async {
    final mock = MockClient((request) async {
      expect(request.url.toString(), startsWith('http://localhost'));
      expect(request.url.path, '/v1/ping');
      return http.Response(
        jsonEncode({
          'code': 0,
          'message': 'success',
          'data': {'x': 1},
        }),
        200,
        headers: {'content-type': 'application/json'},
      );
    });
    final client = ApiClient(
      baseUrl: 'http://localhost',
      httpClient: mock,
    );
    final json = await client.getJson('/v1/ping');
    expect(json['data'], {'x': 1});
    client.dispose();
  });

  test('getJson throws ApiException with status on error', () async {
    final mock = MockClient((request) async {
      return http.Response(
        jsonEncode({'code': 404, 'message': 'not found', 'data': null}),
        404,
        headers: {'content-type': 'application/json'},
      );
    });
    final client = ApiClient(
      baseUrl: 'http://localhost',
      httpClient: mock,
    );
    expect(
      () => client.getJson('/v1/missing'),
      throwsA(
        isA<ApiException>()
            .having((e) => e.statusCode, 'statusCode', 404)
            .having((e) => e.message, 'message', 'not found'),
      ),
    );
    client.dispose();
  });

  test('postJson sends JSON body and Authorization when token set', () async {
    ApiClient.setAuthToken('unit-test-token');
    Map<String, String>? capturedHeaders;
    Object? capturedBody;
    final mock = MockClient((request) async {
      capturedHeaders = Map<String, String>.from(request.headers);
      capturedBody = request.body;
      return http.Response(
        jsonEncode({'code': 0, 'message': 'success', 'data': {'ok': true}}),
        200,
        headers: {'content-type': 'application/json'},
      );
    });
    final client = ApiClient(
      baseUrl: 'http://localhost',
      httpClient: mock,
    );
    await client.postJson(
      '/v1/auth/login',
      body: {'username': 'a', 'password': 'b'},
    );
    final auth = capturedHeaders!['Authorization'] ??
        capturedHeaders!['authorization'];
    expect(auth, 'Bearer unit-test-token');
    final ct = capturedHeaders!['Content-Type'] ??
        capturedHeaders!['content-type'];
    expect(ct, isNotNull);
    expect(ct, contains('application/json'));
    expect(capturedBody, '{"username":"a","password":"b"}');
    client.dispose();
  });
}
