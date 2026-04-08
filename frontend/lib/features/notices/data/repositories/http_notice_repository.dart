import '../../../../core/constants/api_paths.dart';
import '../../../../core/network/api_client.dart';
import '../../../../shared/models/api_response.dart';
import '../../../../shared/models/page_data.dart';
import '../models/notice_models.dart';
import 'notice_repository.dart';

class HttpNoticeRepository implements NoticeRepository {
  final ApiClient apiClient;

  const HttpNoticeRepository({
    required this.apiClient,
  });

  @override
  Future<PageData<NoticeListItemModel>> fetchNotices({
    int page = 1,
    int pageSize = 20,
    String? keyword,
  }) async {
    final json = await apiClient.getJson(
      ApiPaths.notices,
      queryParameters: {
        'page': '$page',
        'page_size': '$pageSize',
      },
    );

    final response = ApiResponse<PageData<NoticeListItemModel>>.fromJson(
      json,
      (rawData) => PageData<NoticeListItemModel>.fromJson(
        rawData as Map<String, dynamic>? ?? {},
        NoticeListItemModel.fromJson,
      ),
    );

    return response.data ??
        const PageData<NoticeListItemModel>(
          items: [],
          total: 0,
          page: 1,
          pageSize: 20,
        );
  }

  @override
  Future<NoticeDetailModel> fetchNoticeDetail(int id) async {
    final json = await apiClient.getJson(ApiPaths.noticeDetail(id));
    final response = ApiResponse<NoticeDetailModel>.fromJson(
      json,
      (rawData) => NoticeDetailModel.fromJson(
        rawData as Map<String, dynamic>? ?? {},
      ),
    );
    return response.data ?? _emptyDetail(id);
  }

  @override
  Future<NoticeSnapshotModel> fetchSnapshot(int id) async {
    final json = await apiClient.getJson(ApiPaths.noticeSnapshot(id));
    final response = ApiResponse<NoticeSnapshotModel>.fromJson(
      json,
      (rawData) => NoticeSnapshotModel.fromJson(
        rawData as Map<String, dynamic>? ?? {},
      ),
    );
    return response.data ??
        const NoticeSnapshotModel(
          id: 0,
          sourceUrl: '',
          sourceSite: '',
          snapshotPath: '',
          content: '',
        );
  }

  NoticeDetailModel _emptyDetail(int id) {
    return NoticeDetailModel(
      id: id,
      title: '',
      summary: '',
      sourceSite: '',
      sourceUrl: '',
      publishedAt: null,
      capturedAt: '',
      qualityScore: 0,
      matchedKeywords: const [],
      isHighPriority: false,
      taskId: 0,
      contentText: '',
      contentHtml: '',
      contentHash: null,
      snapshotPath: null,
    );
  }
}
