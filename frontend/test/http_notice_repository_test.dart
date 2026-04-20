import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:pharma_bid_monitor_frontend/core/network/api_client.dart';
import 'package:pharma_bid_monitor_frontend/features/notices/data/repositories/http_notice_repository.dart';

void main() {
  test('HttpNoticeRepository.fetchNotices adds keyword query', () async {
    final mock = MockClient((request) async {
      expect(request.url.path, '/v1/notices');
      expect(request.url.queryParameters['keyword'], 'kw');
      final body = utf8.encode(
        jsonEncode({
          'code': 0,
          'message': 'success',
          'data': {
            'items': [
              {
                'id': 1,
                'title': 'N1',
                'summary': 'S',
                'source_site': 'src',
                'source_url': 'https://n.example',
                'published_at': null,
                'captured_at': '2024-01-01',
                'quality_score': 8,
                'matched_keywords': ['kw'],
                'is_high_priority': false,
                'task_id': 3,
              },
            ],
            'total': 1,
            'page': 1,
            'page_size': 20,
          },
        }),
      );
      return http.Response.bytes(
        body,
        200,
        headers: {'content-type': 'application/json; charset=utf-8'},
      );
    });
    final client = ApiClient(baseUrl: 'http://localhost', httpClient: mock);
    final repo = HttpNoticeRepository(apiClient: client);
    final page = await repo.fetchNotices(
      page: 1,
      pageSize: 20,
      keyword: 'kw',
    );
    expect(page.total, 1);
    expect(page.items.single.title, 'N1');
    client.dispose();
  });

  test('HttpNoticeRepository.fetchNoticeDetail hits detail path', () async {
    final mock = MockClient((request) async {
      expect(request.url.path, '/v1/notices/7');
      return http.Response(
        jsonEncode({
          'code': 0,
          'message': 'success',
          'data': {
            'id': 7,
            'title': 'Detail',
            'summary': '',
            'source_site': 'x',
            'source_url': 'https://x',
            'published_at': null,
            'captured_at': '2024-01-01',
            'quality_score': 0,
            'matched_keywords': [],
            'is_high_priority': false,
            'task_id': 1,
            'content_text': 'body',
            'content_html': '<p>body</p>',
            'content_hash': null,
            'snapshot_path': null,
          },
        }),
        200,
      );
    });
    final client = ApiClient(baseUrl: 'http://localhost', httpClient: mock);
    final repo = HttpNoticeRepository(apiClient: client);
    final d = await repo.fetchNoticeDetail(7);
    expect(d.id, 7);
    expect(d.title, 'Detail');
    expect(d.contentText, 'body');
    client.dispose();
  });
}
