import '../../../../core/network/api_client.dart';
import '../../../../shared/models/page_data.dart';
import '../models/keyword_rule_model.dart';

class HttpKeywordRuleRepository {
  final ApiClient _apiClient;

  HttpKeywordRuleRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient();

  Future<PageData<KeywordRuleModel>> getKeywordRules({
    int page = 1,
    int pageSize = 100,
  }) async {
    final response = await _apiClient.getJson('/v1/keywords');

    final data = response['data']?['items'] as List<dynamic>? ?? [];
    final items = data
        .map((item) => KeywordRuleModel.fromJson(item as Map<String, dynamic>))
        .toList();
    final total = response['data']?['total'] as int? ?? items.length;

    return PageData(
      items: items,
      total: total,
      page: page,
      pageSize: pageSize,
    );
  }

  Future<KeywordRuleModel> createKeywordRule(KeywordRuleModel rule) async {
    final response = await _apiClient.postJson(
      '/v1/keywords',
      body: rule.toJson(),
    );
    final data = response['data'];
    return KeywordRuleModel.fromJson(data as Map<String, dynamic>);
  }

  Future<KeywordRuleModel> updateKeywordRule(KeywordRuleModel rule) async {
    final response = await _apiClient.putJson(
      '/v1/keywords/${rule.id}',
      body: rule.toJson(),
    );
    final data = response['data'];
    return KeywordRuleModel.fromJson(data as Map<String, dynamic>);
  }

  Future<void> deleteKeywordRule(int id) async {
    await _apiClient.deleteJson('/v1/keywords/$id');
  }

  Future<KeywordRuleModel> toggleKeywordRuleActive(int id) async {
    final response = await _apiClient.postJson('/v1/keywords/$id/toggle');
    final data = response['data'];
    return KeywordRuleModel.fromJson(data as Map<String, dynamic>);
  }
}
