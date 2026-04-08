import re
f = open('c:/Users/WELMAN/Downloads/my_third_app/crawler_system/frontend/lib/features/notices/presentation/pages/notices_page.dart', encoding='utf-8')
content = f.read()
f.close()

before = '''  Future<void> _openSnapshot(\n    BuildContext context,\n    NoticeDetailModel detail,\n  ) async {\n    final messenger = ScaffoldMessenger.of(context);\n    try {\n      final snapshot = await _repository.fetchSnapshot(detail.id);\n      if (!context.mounted) {\n        return;\n      }\n      await showDialog<void>(\n        context: context,\n        builder: (context) {\n          return AlertDialog(\n            title: const Text('快照内容'),\n            content: SizedBox(\n              width: 720,\n              child: SingleChildScrollView(\n                child: SelectableText(snapshot.content),\n              ),\n            ),\n            actions: [\n              TextButton(\n                onPressed: () => Navigator.of(context).pop(),\n                child: const Text('关闭'),\n              ),\n            ],\n          );\n        },\n      );\n    } catch (error) {\n      if (context.mounted) {\n        messenger.showSnackBar(\n          SnackBar(content: Text('加载快照失败：无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“grep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到路径“C:\Users\WELMAN\Downloads\my_third_app\crawler_system\server\.env”，因为该路径不存在。 无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“grep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到与参数名称“Recurse”匹配的参数。 找不到与参数名称“Recurse”匹配的参数。 无法将“grep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到驱动器。名为“http”的驱动器不存在。 System.Management.Automation.ParseException: 所在位置 行:2 字符: 123
+ ... \app\services\notice_service.py | Select-String -Pattern "def _to_not ...
+                                                               ~~~
表达式或语句中包含意外的标记“def”。

所在位置 行:3 字符: 116
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。

所在位置 行:3 字符: 160
+ ... ces\notice_service.py', 'r', encoding='utf-8') as f: print(f.read())"
+                                                                       ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f{j+1}: {lines[j]}”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 12
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+            ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 30
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                              ~
“,”后面缺少表达式。

所在位置 行:1 字符: 31
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                               ~~~
表达式或语句中包含意外的标记“i-5”。

所在位置 行:1 字符: 30
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                              ~
表达式中缺少右“)”。

所在位置 行:1 字符: 58
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                                                          ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 7
+     if '_to_notice_list_item' in line:
+       ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 31
+     if '_to_notice_list_item' in line:
+                               ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for i, line in enumerate(lines):
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 6
+ for i, line in enumerate(lines):
+      ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“lines”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 18
+ asyncio.run(main())
+                  ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+         traceback.print_exc()
+                             ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 40
+             stats = await ds.get_stats()
+                                        ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 47
+             res = await ns.list_notices(page=1, page_size=10)
+                                               ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 36
+             ns = NoticeService(repo, kw_repo)
+                                    ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 38
+         async with AsyncSessionLocal() as session:
+                                      ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 16
+ async def main():
+                ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.task_repo import TaskRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.log_repo import LogRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.dashboard_service import DashboardService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.notice_service import NoticeService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.keyword_rule_repo import KeywordRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.data_repo import DataRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.core.database import AsyncSessionLocal
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+ sys.path.insert(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_s ...
+                   ~
“,”后面缺少表达式。

所在位置 行:1 字符: 20
+ ... h.insert(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_system\s ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
表达式或语句中包含意外的标记“r'c:\Users\WELMAN\Downloads\my_third_app\crawler_system\server'”。

所在位置 行:1 字符: 19
+ sys.path.insert(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_s ...
+                   ~
表达式中缺少右“)”。

所在位置 行:1 字符: 83
+ ... t(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_system\server')
+                                                                         ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“pass”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 3
+ if __name__ == '__main__':
+   ~
if 语句中的“if”后面缺少“(”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+         traceback.print_exc()
+                             ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 35
+             print('Stats recent:', len(stats.recent_notices))
+                                   ~
“,”后面缺少表达式。

所在位置 行:1 字符: 36
+             print('Stats recent:', len(stats.recent_notices))
+                                    ~~~
表达式或语句中包含意外的标记“len”。

所在位置 行:1 字符: 35
+             print('Stats recent:', len(stats.recent_notices))
+                                   ~
表达式中缺少右“)”。

所在位置 行:1 字符: 61
+             print('Stats recent:', len(stats.recent_notices))
+                                                             ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 40
+             stats = await ds.get_stats()
+                                        ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 37
+             print('Notices length:', len(res.items))
+                                     ~
“,”后面缺少表达式。

所在位置 行:1 字符: 38
+             print('Notices length:', len(res.items))
+                                      ~~~
表达式或语句中包含意外的标记“len”。

所在位置 行:1 字符: 37
+             print('Notices length:', len(res.items))
+                                     ~
表达式中缺少右“)”。

所在位置 行:1 字符: 52
+             print('Notices length:', len(res.items))
+                                                    ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 47
+             res = await ns.list_notices(page=1, page_size=10)
+                                               ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 36
+             ns = NoticeService(repo, kw_repo)
+                                    ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 38
+         async with AsyncSessionLocal() as session:
+                                      ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 16
+ async def main():
+                ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.core.database import AsyncSessionLocal
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.task_repo import TaskRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.log_repo import LogRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.dashboard_service import DashboardService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.notice_service import NoticeService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.keyword_rule_repo import KeywordRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.data_repo import DataRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from sqlalchemy.orm import sessionmaker
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+     print('Notices Error:', e)
+                            ~
“,”后面缺少表达式。

所在位置 行:1 字符: 29
+     print('Notices Error:', e)
+                             ~
表达式或语句中包含意外的标记“e”。

所在位置 行:1 字符: 28
+     print('Notices Error:', e)
+                            ~
表达式中缺少右“)”。

所在位置 行:1 字符: 30
+     print('Notices Error:', e)
+                              ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+     print('Notices Status:', res.getcode())
+                             ~
“,”后面缺少表达式。

所在位置 行:1 字符: 30
+     print('Notices Status:', res.getcode())
+                              ~~~~~~~~~~~
表达式或语句中包含意外的标记“res.getcode”。

所在位置 行:1 字符: 29
+     print('Notices Status:', res.getcode())
+                             ~
表达式中缺少右“)”。

所在位置 行:1 字符: 42
+     print('Notices Status:', res.getcode())
+                                          ~
“(”后面应为表达式。

所在位置 行:1 字符: 43
+     print('Notices Status:', res.getcode())
+                                           ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“res”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 30
+     print('Dashboard Error:', e)
+                              ~
“,”后面缺少表达式。

所在位置 行:1 字符: 31
+     print('Dashboard Error:', e)
+                               ~
表达式或语句中包含意外的标记“e”。

所在位置 行:1 字符: 30
+     print('Dashboard Error:', e)
+                              ~
表达式中缺少右“)”。

所在位置 行:1 字符: 32
+     print('Dashboard Error:', e)
+                                ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 31
+     print('Dashboard Status:', res.getcode())
+                               ~
“,”后面缺少表达式。

所在位置 行:1 字符: 32
+     print('Dashboard Status:', res.getcode())
+                                ~~~~~~~~~~~
表达式或语句中包含意外的标记“res.getcode”。

所在位置 行:1 字符: 31
+     print('Dashboard Status:', res.getcode())
+                               ~
表达式中缺少右“)”。

所在位置 行:1 字符: 44
+     print('Dashboard Status:', res.getcode())
+                                            ~
“(”后面应为表达式。

所在位置 行:1 字符: 45
+     print('Dashboard Status:', res.getcode())
+                                             ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“res”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:2 字符: 78
+ ... ownloads\my_third_app\crawler_system\server ; python -c "from main im ...
+                                                              ~~~~
表达式或语句中包含意外的标记“from”。

所在位置 行:2 字符: 78
+ ... ownloads\my_third_app\crawler_system\server ; python -c "from main im ...
+                                                              ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(init_new, init_old)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“init_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“init_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(sig_new, sig_old)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“sig_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“sig_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 25
+ text = text.replace(cols, '    quality_score: Mapped[int] = mapped_co ...
+                         ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“cols”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_call, new_call)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_heat, new_heat)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_heat”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_heat”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_call, new_call)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 32
+ text = text.replace(old_to_list, new_to_list)
+                                ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_calc, new_calc)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_calc”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_calc”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_init, new_init)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_init”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_init”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 98
+ ... \my_third_app\crawler_system\server\app\api\v1\dashboard.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(old_dep, new_dep)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 98
+ ... \my_third_app\crawler_system\server\app\api\v1\dashboard.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 95
+ ... ads\my_third_app\crawler_system\server\app\api\v1\notice.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(old_dep, new_dep)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 95
+ ... ads\my_third_app\crawler_system\server\app\api\v1\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 32
+ text = text.replace(old_to_list, new_to_list)
+                                ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(old_get, new_get)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_get”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_get”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_list, new_list)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 30
+ text = text.replace(old_func2, new_func2)
+                              ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_func2”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_func2”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 30
+ text = text.replace(old_func1, new_func1)
+                              ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_func1”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_func1”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f{i+1}: {line}”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for i, line in enumerate(lines[:100]):
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 6
+ for i, line in enumerate(lines[:100]):
+      ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“lines”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 18
+     print(f.read()[:500])
+                  ~
“(”后面应为表达式。

所在位置 行:1 字符: 20
+     print(f.read()[:500])
+                    ~
数组索引表达式丢失或无效。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 96
+ ... ds\my_third_app\crawler_system\server\app\schemas\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(init_old, init_new)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“init_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“init_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(sig_old, sig_new)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“sig_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“sig_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f.write”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到驱动器。名为“import 'package”的驱动器不存在。 找不到驱动器。名为“Set-Content -Path "c”的驱动器不存在。 找不到驱动器。名为“cat c”的驱动器不存在。 找不到驱动器。名为“cat c”的驱动器不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“cat c”的驱动器不存在。 找不到驱动器。名为“Get-ChildItem -Path c”的驱动器不存在。 找不到驱动器。名为“Get-ChildItem -Path c”的驱动器不存在。 找不到路径“C:\Users\WELMAN\Downloads\my_third_app\crawler_system\frontend\ls lib\features\keyword_rules -R”，因为该路径不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“python -c "import urllib.request; print(urllib.request.urlopen('http”的驱动器不存在。 找不到驱动器。名为“curl -s http”的驱动器不存在。 找不到驱动器。名为“python -c "import urllib.request; print(urllib.request.urlopen('http”的驱动器不存在。 指定路径 curl -s http://127.0.0.1:8000/api/v1/health 处的某个对象不存在，或者已被 -Include 或 -Exclude 参数过滤掉。 找不到驱动器。名为“curl -s http”的驱动器不存在。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 112
+ ... ed[int] = mapped_column(Integer, nullable=False, default=0)', add_col ...
+                                                                  ~
“,”后面缺少表达式。

所在位置 行:1 字符: 113
+ ... t] = mapped_column(Integer, nullable=False, default=0)', add_columns)
+                                                              ~~~~~~~~~~~
表达式或语句中包含意外的标记“add_columns”。

所在位置 行:1 字符: 112
+ ... ed[int] = mapped_column(Integer, nullable=False, default=0)', add_col ...
+                                                                  ~
表达式中缺少右“)”。

所在位置 行:1 字符: 124
+ ... t] = mapped_column(Integer, nullable=False, default=0)', add_columns)
+                                                                         ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“add_columns”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 22
+     content = f.read()
+                      ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f{i+1}: {line}”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for i, line in enumerate(lines[:100]):
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 6
+ for i, line in enumerate(lines[:100]):
+      ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“lines”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:5 字符: 15
+ Write-Output "test"
+               ~~~~~
表达式或语句中包含意外的标记“test"
cmd /c "dir”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for f in os.listdir(r'c:\Users\WELMAN\Downloads\my_third_app\crawler_ ...
+    ~
关键字“for”后面缺少左“(”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“rc:\Users\WELMAN\Downloads\my_third_app\crawler_system\server\app\services”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 36
+             print(os.path.join(root, file))
+                                    ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 11
+         if file.endswith('.py') and ('pipeline' in file or 'crawl' in ...
+           ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 49
+         if file.endswith('.py') and ('pipeline' in file or 'crawl' in ...
+                                                 ~~
表达式或语句中包含意外的标记“in”。

所在位置 行:1 字符: 48
+         if file.endswith('.py') and ('pipeline' in file or 'crawl' in ...
+                                                ~
表达式中缺少右“)”。

所在位置 行:1 字符: 93
+ ... '.py') and ('pipeline' in file or 'crawl' in file or 'data' in file):
+                                                                        ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 8
+     for file in files:
+        ~
关键字“for”后面缺少左“(”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for root, dirs, files in os.walk(r'c:\Users\WELMAN\Downloads\my_third ...
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 9
+ for root, dirs, files in os.walk(r'c:\Users\WELMAN\Downloads\my_third ...
+         ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 18
+     print(f.read()[:1000])
+                  ~
“(”后面应为表达式。

所在位置 行:1 字符: 20
+     print(f.read()[:1000])
+                    ~
数组索引表达式丢失或无效。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\services\crawl_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 27
+             with open(path, 'w', encoding='utf-8') as file:
+                           ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 找不到接受实际参数“content.replace”的位置形式参数。 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 15
+             if 'app.api.v1.keyword ' in content or 'from app.api.v1 i ...
+               ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 38
+             if 'app.api.v1.keyword ' in content or 'from app.api.v1 i ...
+                                      ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 15
+             if 'app.services.keyword_service' in content:
+               ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 47
+             if 'app.services.keyword_service' in content:
+                                               ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 15
+             if 'app.repositories.keyword_repo' in content:
+               ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 48
+             if 'app.repositories.keyword_repo' in content:
+                                                ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 {"code":404,"message":"Not Found","data":null} 只应将 ScriptBlock 指定为 Command 参数值。')),\n        );\n      }\n    }\n  }'''
after = '''  Future<void> _openSnapshot(\n    BuildContext context,\n    NoticeDetailModel detail, [\n    String? keywordToHighlight,\n  ]) async {\n    final messenger = ScaffoldMessenger.of(context);\n    try {\n      final snapshot = await _repository.fetchSnapshot(detail.id);\n      if (!context.mounted) {\n        return;\n      }\n      await showDialog<void>(\n        context: context,\n        builder: (context) {\n          return _SnapshotViewerDialog(\n            content: snapshot.content,\n            keywordToHighlight: keywordToHighlight,\n          );\n        },\n      );\n    } catch (error) {\n      if (context.mounted) {\n        messenger.showSnackBar(\n          SnackBar(content: Text('加载快照失败：无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“grep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到路径“C:\Users\WELMAN\Downloads\my_third_app\crawler_system\server\.env”，因为该路径不存在。 无法将“head”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“grep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到与参数名称“Recurse”匹配的参数。 找不到与参数名称“Recurse”匹配的参数。 无法将“grep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到驱动器。名为“http”的驱动器不存在。 System.Management.Automation.ParseException: 所在位置 行:2 字符: 123
+ ... \app\services\notice_service.py | Select-String -Pattern "def _to_not ...
+                                                               ~~~
表达式或语句中包含意外的标记“def”。

所在位置 行:3 字符: 116
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。

所在位置 行:3 字符: 160
+ ... ces\notice_service.py', 'r', encoding='utf-8') as f: print(f.read())"
+                                                                       ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f{j+1}: {lines[j]}”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 12
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+            ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 30
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                              ~
“,”后面缺少表达式。

所在位置 行:1 字符: 31
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                               ~~~
表达式或语句中包含意外的标记“i-5”。

所在位置 行:1 字符: 30
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                              ~
表达式中缺少右“)”。

所在位置 行:1 字符: 58
+         for j in range(max(0, i-5), min(len(lines), i+15)):
+                                                          ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 7
+     if '_to_notice_list_item' in line:
+       ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 31
+     if '_to_notice_list_item' in line:
+                               ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for i, line in enumerate(lines):
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 6
+ for i, line in enumerate(lines):
+      ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“lines”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 18
+ asyncio.run(main())
+                  ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+         traceback.print_exc()
+                             ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 40
+             stats = await ds.get_stats()
+                                        ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 47
+             res = await ns.list_notices(page=1, page_size=10)
+                                               ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 36
+             ns = NoticeService(repo, kw_repo)
+                                    ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 38
+         async with AsyncSessionLocal() as session:
+                                      ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 16
+ async def main():
+                ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.task_repo import TaskRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.log_repo import LogRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.dashboard_service import DashboardService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.notice_service import NoticeService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.keyword_rule_repo import KeywordRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.data_repo import DataRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.core.database import AsyncSessionLocal
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+ sys.path.insert(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_s ...
+                   ~
“,”后面缺少表达式。

所在位置 行:1 字符: 20
+ ... h.insert(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_system\s ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
表达式或语句中包含意外的标记“r'c:\Users\WELMAN\Downloads\my_third_app\crawler_system\server'”。

所在位置 行:1 字符: 19
+ sys.path.insert(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_s ...
+                   ~
表达式中缺少右“)”。

所在位置 行:1 字符: 83
+ ... t(0, r'c:\Users\WELMAN\Downloads\my_third_app\crawler_system\server')
+                                                                         ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“pass”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 3
+ if __name__ == '__main__':
+   ~
if 语句中的“if”后面缺少“(”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+         traceback.print_exc()
+                             ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 35
+             print('Stats recent:', len(stats.recent_notices))
+                                   ~
“,”后面缺少表达式。

所在位置 行:1 字符: 36
+             print('Stats recent:', len(stats.recent_notices))
+                                    ~~~
表达式或语句中包含意外的标记“len”。

所在位置 行:1 字符: 35
+             print('Stats recent:', len(stats.recent_notices))
+                                   ~
表达式中缺少右“)”。

所在位置 行:1 字符: 61
+             print('Stats recent:', len(stats.recent_notices))
+                                                             ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 40
+             stats = await ds.get_stats()
+                                        ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 37
+             print('Notices length:', len(res.items))
+                                     ~
“,”后面缺少表达式。

所在位置 行:1 字符: 38
+             print('Notices length:', len(res.items))
+                                      ~~~
表达式或语句中包含意外的标记“len”。

所在位置 行:1 字符: 37
+             print('Notices length:', len(res.items))
+                                     ~
表达式中缺少右“)”。

所在位置 行:1 字符: 52
+             print('Notices length:', len(res.items))
+                                                    ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 47
+             res = await ns.list_notices(page=1, page_size=10)
+                                               ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 36
+             ns = NoticeService(repo, kw_repo)
+                                    ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“session”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 38
+         async with AsyncSessionLocal() as session:
+                                      ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 16
+ async def main():
+                ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.core.database import AsyncSessionLocal
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.task_repo import TaskRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.log_repo import LogRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.dashboard_service import DashboardService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.services.notice_service import NoticeService
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.keyword_rule_repo import KeywordRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from app.repositories.data_repo import DataRepository
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from sqlalchemy.orm import sessionmaker
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 1
+ from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
+ ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+     print('Notices Error:', e)
+                            ~
“,”后面缺少表达式。

所在位置 行:1 字符: 29
+     print('Notices Error:', e)
+                             ~
表达式或语句中包含意外的标记“e”。

所在位置 行:1 字符: 28
+     print('Notices Error:', e)
+                            ~
表达式中缺少右“)”。

所在位置 行:1 字符: 30
+     print('Notices Error:', e)
+                              ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+     print('Notices Status:', res.getcode())
+                             ~
“,”后面缺少表达式。

所在位置 行:1 字符: 30
+     print('Notices Status:', res.getcode())
+                              ~~~~~~~~~~~
表达式或语句中包含意外的标记“res.getcode”。

所在位置 行:1 字符: 29
+     print('Notices Status:', res.getcode())
+                             ~
表达式中缺少右“)”。

所在位置 行:1 字符: 42
+     print('Notices Status:', res.getcode())
+                                          ~
“(”后面应为表达式。

所在位置 行:1 字符: 43
+     print('Notices Status:', res.getcode())
+                                           ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“res”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 30
+     print('Dashboard Error:', e)
+                              ~
“,”后面缺少表达式。

所在位置 行:1 字符: 31
+     print('Dashboard Error:', e)
+                               ~
表达式或语句中包含意外的标记“e”。

所在位置 行:1 字符: 30
+     print('Dashboard Error:', e)
+                              ~
表达式中缺少右“)”。

所在位置 行:1 字符: 32
+     print('Dashboard Error:', e)
+                                ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“except”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 31
+     print('Dashboard Status:', res.getcode())
+                               ~
“,”后面缺少表达式。

所在位置 行:1 字符: 32
+     print('Dashboard Status:', res.getcode())
+                                ~~~~~~~~~~~
表达式或语句中包含意外的标记“res.getcode”。

所在位置 行:1 字符: 31
+     print('Dashboard Status:', res.getcode())
+                               ~
表达式中缺少右“)”。

所在位置 行:1 字符: 44
+     print('Dashboard Status:', res.getcode())
+                                            ~
“(”后面应为表达式。

所在位置 行:1 字符: 45
+     print('Dashboard Status:', res.getcode())
+                                             ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“res”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“try:”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:2 字符: 78
+ ... ownloads\my_third_app\crawler_system\server ; python -c "from main im ...
+                                                              ~~~~
表达式或语句中包含意外的标记“from”。

所在位置 行:2 字符: 78
+ ... ownloads\my_third_app\crawler_system\server ; python -c "from main im ...
+                                                              ~~~~
此语言版本中不支持“from”关键字。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(init_new, init_old)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“init_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“init_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(sig_new, sig_old)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“sig_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“sig_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 25
+ text = text.replace(cols, '    quality_score: Mapped[int] = mapped_co ...
+                         ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“cols”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_call, new_call)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_heat, new_heat)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_heat”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_heat”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_call, new_call)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_call”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 32
+ text = text.replace(old_to_list, new_to_list)
+                                ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_calc, new_calc)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_calc”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_calc”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_init, new_init)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_init”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_init”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 108
+ ... app\crawler_system\server\app\services\dashboard_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 98
+ ... \my_third_app\crawler_system\server\app\api\v1\dashboard.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(old_dep, new_dep)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 98
+ ... \my_third_app\crawler_system\server\app\api\v1\dashboard.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 95
+ ... ads\my_third_app\crawler_system\server\app\api\v1\notice.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(old_dep, new_dep)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_dep”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 95
+ ... ads\my_third_app\crawler_system\server\app\api\v1\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 32
+ text = text.replace(old_to_list, new_to_list)
+                                ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_to_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(old_get, new_get)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_get”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_get”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(old_list, new_list)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_list”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 30
+ text = text.replace(old_func2, new_func2)
+                              ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_func2”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_func2”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 30
+ text = text.replace(old_func1, new_func1)
+                              ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“new_func1”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“old_func1”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 94
+ ... oads\my_third_app\crawler_system\server\app\utils\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f{i+1}: {line}”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for i, line in enumerate(lines[:100]):
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 6
+ for i, line in enumerate(lines[:100]):
+      ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“lines”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 105
+ ... rd_app\crawler_system\server\app\services\notice_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 18
+     print(f.read()[:500])
+                  ~
“(”后面应为表达式。

所在位置 行:1 字符: 20
+     print(f.read()[:500])
+                    ~
数组索引表达式丢失或无效。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 96
+ ... ds\my_third_app\crawler_system\server\app\schemas\notice.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“text”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 29
+ text = text.replace(init_old, init_new)
+                             ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“init_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“init_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 28
+ text = text.replace(sig_old, sig_new)
+                            ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“sig_new”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“sig_old”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f.write”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到驱动器。名为“import 'package”的驱动器不存在。 找不到驱动器。名为“Set-Content -Path "c”的驱动器不存在。 找不到驱动器。名为“cat c”的驱动器不存在。 找不到驱动器。名为“cat c”的驱动器不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“cat c”的驱动器不存在。 找不到驱动器。名为“Get-ChildItem -Path c”的驱动器不存在。 找不到驱动器。名为“Get-ChildItem -Path c”的驱动器不存在。 找不到路径“C:\Users\WELMAN\Downloads\my_third_app\crawler_system\frontend\ls lib\features\keyword_rules -R”，因为该路径不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“cd c”的驱动器不存在。 找不到驱动器。名为“python -c "import urllib.request; print(urllib.request.urlopen('http”的驱动器不存在。 找不到驱动器。名为“curl -s http”的驱动器不存在。 找不到驱动器。名为“python -c "import urllib.request; print(urllib.request.urlopen('http”的驱动器不存在。 指定路径 curl -s http://127.0.0.1:8000/api/v1/health 处的某个对象不存在，或者已被 -Include 或 -Exclude 参数过滤掉。 找不到驱动器。名为“curl -s http”的驱动器不存在。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'w', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 112
+ ... ed[int] = mapped_column(Integer, nullable=False, default=0)', add_col ...
+                                                                  ~
“,”后面缺少表达式。

所在位置 行:1 字符: 113
+ ... t] = mapped_column(Integer, nullable=False, default=0)', add_columns)
+                                                              ~~~~~~~~~~~
表达式或语句中包含意外的标记“add_columns”。

所在位置 行:1 字符: 112
+ ... ed[int] = mapped_column(Integer, nullable=False, default=0)', add_col ...
+                                                                  ~
表达式中缺少右“)”。

所在位置 行:1 字符: 124
+ ... t] = mapped_column(Integer, nullable=False, default=0)', add_columns)
+                                                                         ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“add_columns”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 22
+     content = f.read()
+                      ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 93
+ ... loads\my_third_app\crawler_system\server\app\models\data.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f{i+1}: {line}”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for i, line in enumerate(lines[:100]):
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 6
+ for i, line in enumerate(lines[:100]):
+      ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“lines”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 19
+     text = f.read()
+                   ~
“(”后面应为表达式。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\repositories\data_repo.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:5 字符: 15
+ Write-Output "test"
+               ~~~~~
表达式或语句中包含意外的标记“test"
cmd /c "dir”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“f”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for f in os.listdir(r'c:\Users\WELMAN\Downloads\my_third_app\crawler_ ...
+    ~
关键字“for”后面缺少左“(”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“rc:\Users\WELMAN\Downloads\my_third_app\crawler_system\server\app\services”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 36
+             print(os.path.join(root, file))
+                                    ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 11
+         if file.endswith('.py') and ('pipeline' in file or 'crawl' in ...
+           ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 49
+         if file.endswith('.py') and ('pipeline' in file or 'crawl' in ...
+                                                 ~~
表达式或语句中包含意外的标记“in”。

所在位置 行:1 字符: 48
+         if file.endswith('.py') and ('pipeline' in file or 'crawl' in ...
+                                                ~
表达式中缺少右“)”。

所在位置 行:1 字符: 93
+ ... '.py') and ('pipeline' in file or 'crawl' in file or 'data' in file):
+                                                                        ~
表达式或语句中包含意外的标记“)”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 8
+     for file in files:
+        ~
关键字“for”后面缺少左“(”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 4
+ for root, dirs, files in os.walk(r'c:\Users\WELMAN\Downloads\my_third ...
+    ~
关键字“for”后面缺少左“(”。

所在位置 行:1 字符: 9
+ for root, dirs, files in os.walk(r'c:\Users\WELMAN\Downloads\my_third ...
+         ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 无法将“import”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 18
+     print(f.read()[:1000])
+                  ~
“(”后面应为表达式。

所在位置 行:1 字符: 20
+     print(f.read()[:1000])
+                    ~
数组索引表达式丢失或无效。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 104
+ ... ird_app\crawler_system\server\app\services\crawl_service.py', 'r', en ...
+                                                                 ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) System.Management.Automation.ParseException: 所在位置 行:1 字符: 27
+             with open(path, 'w', encoding='utf-8') as file:
+                           ~
参数列表中缺少参量。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 找不到接受实际参数“content.replace”的位置形式参数。 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 15
+             if 'app.api.v1.keyword ' in content or 'from app.api.v1 i ...
+               ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 38
+             if 'app.api.v1.keyword ' in content or 'from app.api.v1 i ...
+                                      ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 15
+             if 'app.services.keyword_service' in content:
+               ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 47
+             if 'app.services.keyword_service' in content:
+                                               ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 System.Management.Automation.ParseException: 所在位置 行:1 字符: 15
+             if 'app.repositories.keyword_repo' in content:
+               ~
if 语句中的“if”后面缺少“(”。

所在位置 行:1 字符: 48
+             if 'app.repositories.keyword_repo' in content:
+                                                ~~
表达式或语句中包含意外的标记“in”。
   在 System.Management.Automation.Runspaces.PipelineBase.Invoke(IEnumerable input)
   在 Microsoft.PowerShell.Executor.ExecuteCommandHelper(Pipeline tempPipeline, Exception& exceptionThrown, ExecutionOptions options) 找不到接受实际参数“content.replace”的位置形式参数。 {"code":404,"message":"Not Found","data":null} 只应将 ScriptBlock 指定为 Command 参数值。')),\n        );\n      }\n    }\n  }'''
\ncontent = content.replace(before, after)\nif after in content:\n  print('Replaced')\nelse:\n  print('Not replaced!')

f = open('c:/Users/WELMAN/Downloads/my_third_app/crawler_system/frontend/lib/features/notices/presentation/pages/notices_page.dart', 'w', encoding='utf-8')
f.write(content)
f.close()
