import 'dart:typed_data';

/// 非 Web / 非 IO 平台占位。
Future<String?> triggerFileDownload(Uint8List bytes, String filename) async {
  return null;
}
