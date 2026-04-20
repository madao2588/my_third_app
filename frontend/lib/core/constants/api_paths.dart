class ApiPaths {
  static const dashboardOverview = '/v1/dashboard/overview';
  static const dataExportCsv = '/v1/data/export/csv';
  static const notices = '/v1/notices';
  static const tasks = '/v1/tasks';
  static const logs = '/v1/logs';
  static const logSummary = '/v1/logs/summary';
  static const taskTemplates = '/v1/templates/tasks';
  static const testTemplate = '/v1/templates/test';
  static const statsOverview = '/v1/stats/overview';

  static String noticeDetail(int id) => '/v1/notices/$id';
  static String taskDetail(int id) => '/v1/tasks/$id';
  static String useTaskTemplate(String id) => '/v1/templates/tasks/$id/use';

  static String noticeSnapshot(int id) => '/v1/notices/$id/snapshot';

  static String runTask(int id) => '/v1/tasks/$id/run';
}
