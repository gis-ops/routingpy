import requests

r = requests.get("http://localhost:8082/get", {"a": "b"})
print(r.json())
