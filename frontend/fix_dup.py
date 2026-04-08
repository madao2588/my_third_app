f = open('c:/Users/WELMAN/Downloads/my_third_app/crawler_system/frontend/lib/features/notices/presentation/pages/notices_page.dart', encoding='utf-8')
content = f.read()
f.close()

idx = content.rfind('class _SnapshotViewerDialog extends StatefulWidget')
content = content[:idx]
f = open('c:/Users/WELMAN/Downloads/my_third_app/crawler_system/frontend/lib/features/notices/presentation/pages/notices_page.dart', 'w', encoding='utf-8')
f.write(content)
f.close()
