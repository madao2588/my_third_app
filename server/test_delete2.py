import urllib.request; import urllib.error; req = urllib.request.Request('http://127.0.0.1:8000/v1/tasks/4', method='DELETE');
try:
  urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
  print(e.read().decode())
