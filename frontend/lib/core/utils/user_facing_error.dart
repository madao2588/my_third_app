import 'dart:async';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../network/api_client.dart';

bool _containsHan(String s) => RegExp(r'[\u4e00-\u9fff]').hasMatch(s);

String _httpStatusHint(int code) {
  if (code >= 500 && code < 600) {
    return '服务器暂时不可用，请稍后重试。';
  }
  return switch (code) {
    400 => '请求无效，请检查填写内容。',
    401 => '未授权或登录已失效，请检查账号密码或重新登录。',
    403 => '没有权限执行此操作。',
    404 => '请求的资源不存在。',
    408 => '请求超时，请稍后重试。',
    409 => '与当前数据状态冲突，请刷新后重试。',
    422 => '提交的数据未通过校验，请检查表单。',
    429 => '请求过于频繁，请稍后再试。',
    _ => '请求失败（HTTP $code）。',
  };
}

String _apiExceptionCopy(ApiException error) {
  final raw = error.message.trim();
  final code = error.statusCode;

  if (raw.isEmpty) {
    return code == null ? '请求失败。' : _httpStatusHint(code);
  }

  if (_containsHan(raw)) {
    return raw;
  }

  final lower = raw.toLowerCase();
  final generic = lower == 'request failed' ||
      lower == 'internal server error' ||
      lower == 'validation error' ||
      lower == 'request failed (401)' ||
      lower == 'unauthorized' ||
      lower == 'forbidden' ||
      lower == 'not found';

  if (generic && code != null) {
    return _httpStatusHint(code);
  }

  if (code == 401 &&
      (lower.contains('unauthorized') ||
          lower.contains('authorization') ||
          lower.contains('invalid token'))) {
    return '登录已失效或账号密码错误，请重新登录。';
  }

  if (code != null && raw.length < 80 && !_containsHan(raw)) {
    return '${_httpStatusHint(code)}（$raw）';
  }

  return raw;
}

/// Maps exceptions from [ApiClient] / HTTP / JSON decode to short Chinese copy.
String userFacingError(Object? error) {
  if (error == null) {
    return '发生未知错误，请稍后重试。';
  }
  if (error is ApiException) {
    return _apiExceptionCopy(error);
  }
  if (error is TimeoutException) {
    return '请求超时，请确认本机网络及后端服务是否可用。';
  }
  if (error is SocketException) {
    return '无法连接到服务器，请确认后端已启动，且「接口地址」配置正确。';
  }
  if (error is http.ClientException) {
    final m = error.message.trim();
    return m.isEmpty ? '网络连接异常，请稍后重试。' : '网络异常：$m';
  }
  if (error is FormatException) {
    return '服务器返回了无法解析的数据，请稍后重试。';
  }
  return '操作失败：$error';
}
