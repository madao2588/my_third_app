import 'dart:async';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pharma_bid_monitor_frontend/core/network/api_client.dart';
import 'package:pharma_bid_monitor_frontend/core/utils/user_facing_error.dart';

void main() {
  test('ApiException with Chinese message is preserved', () {
    expect(
      userFacingError(const ApiException('用户名或密码错误', statusCode: 401)),
      '用户名或密码错误',
    );
  });

  test('generic 401 maps to auth hint', () {
    expect(
      userFacingError(const ApiException('Unauthorized', statusCode: 401)),
      '未授权或登录已失效，请检查账号密码或重新登录。',
    );
  });

  test('401 invalid token uses dedicated copy', () {
    expect(
      userFacingError(
        const ApiException('Invalid token format', statusCode: 401),
      ),
      '登录已失效或账号密码错误，请重新登录。',
    );
  });

  test('5xx generic message maps to server unavailable', () {
    expect(
      userFacingError(
        const ApiException('internal server error', statusCode: 503),
      ),
      '服务器暂时不可用，请稍后重试。',
    );
  });

  test('TimeoutException', () {
    expect(
      userFacingError(TimeoutException('x')),
      contains('超时'),
    );
  });

  test('SocketException mentions backend', () {
    expect(
      userFacingError(const SocketException('failed')),
      contains('后端'),
    );
  });

  test('http ClientException', () {
    expect(
      userFacingError(http.ClientException('refused')),
      contains('网络'),
    );
  });
}
