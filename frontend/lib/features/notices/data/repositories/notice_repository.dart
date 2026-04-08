import '../../../../shared/models/page_data.dart';
import '../models/notice_models.dart';

abstract class NoticeRepository {
  Future<PageData<NoticeListItemModel>> fetchNotices({
    int page = 1,
    int pageSize = 20,
    String? keyword,
  });

  Future<NoticeDetailModel> fetchNoticeDetail(int id);

  Future<NoticeSnapshotModel> fetchSnapshot(int id);
}
