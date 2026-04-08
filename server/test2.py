import urllib.request; req = urllib.request.Request('http://127.0.0.1:8000/v1/tasks/4', method='DELETE'); res = urllib.request.urlopen(req); print(res.status, res.read().decode())
