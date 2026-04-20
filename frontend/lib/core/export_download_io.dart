import 'dart:io';
import 'dart:typed_data';

Future<String?> triggerFileDownload(Uint8List bytes, String filename) async {
  final path = '${Directory.systemTemp.path}/$filename';
  final file = File(path);
  await file.writeAsBytes(bytes, flush: true);
  return path;
}
