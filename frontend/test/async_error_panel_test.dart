import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pharma_bid_monitor_frontend/core/network/api_client.dart';
import 'package:pharma_bid_monitor_frontend/core/widgets/async_error_panel.dart';

void main() {
  testWidgets('AsyncErrorPanel shows title, message and retry', (tester) async {
    var retried = false;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AsyncErrorPanel(
            error: const ApiException('internal server error', statusCode: 503),
            title: '加载失败',
            onRetry: () {
              retried = true;
            },
          ),
        ),
      ),
    );

    expect(find.text('加载失败'), findsOneWidget);
    expect(find.text('重试'), findsOneWidget);

    await tester.tap(find.text('重试'));
    await tester.pump();
    expect(retried, isTrue);
  });

  testWidgets('AsyncErrorPanel without onRetry hides button', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: AsyncErrorPanel(
            error: ApiException('仅提示', statusCode: 400),
            title: '出错了',
          ),
        ),
      ),
    );

    expect(find.text('出错了'), findsOneWidget);
    expect(find.text('重试'), findsNothing);
  });
}
