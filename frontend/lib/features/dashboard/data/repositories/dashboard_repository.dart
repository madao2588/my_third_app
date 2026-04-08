import '../models/dashboard_models.dart';

abstract class DashboardRepository {
  Future<DashboardOverviewModel> fetchOverview();
}
