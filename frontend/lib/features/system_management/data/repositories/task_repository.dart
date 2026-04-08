import '../../../../shared/models/page_data.dart';
import '../models/task_models.dart';

abstract class TaskRepository {
  Future<PageData<TaskListItemModel>> fetchTasks({
    int page = 1,
    int pageSize = 20,
  });

  Future<TaskListItemModel> createTask(TaskUpsertPayload payload);

  Future<TaskListItemModel> fetchTask(int id);

  Future<TaskListItemModel> updateTask(int id, TaskUpsertPayload payload);

  Future<void> deleteTask(int id);

  Future<TaskRunResultModel> runTask(int id);

  Future<PageData<TaskLogItemModel>> fetchTaskLogs(
    int taskId, {
    int page = 1,
    int pageSize = 10,
  });

  Future<PageData<TaskLogItemModel>> fetchLogs({
    int page = 1,
    int pageSize = 20,
    int? taskId,
    String? level,
  });

  Future<LogSummaryModel> fetchLogSummary();
}
