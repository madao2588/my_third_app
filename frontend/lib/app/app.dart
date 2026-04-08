import 'package:flutter/material.dart';

import '../core/theme/app_theme.dart';
import 'router/app_router.dart';

class PharmaBidMonitorApp extends StatelessWidget {
  const PharmaBidMonitorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '制药招标监测系统',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light(),
      home: const AppRouter(),
    );
  }
}
