import requests
import json

BASE = "http://127.0.0.1:8003/api"

resp = requests.post(f"{BASE}/auth/login", json={"email": "admin@test.com", "password": "123456"})
token = resp.json()["token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

with open("articles_data.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

success = 0
for a in articles:
    resp = requests.post(f"{BASE}/admin/articles", json=a, headers=headers)
    if resp.status_code in (200, 201):
        print(f"OK: {a['title']}")
        success += 1
    else:
        print(f"FAIL ({resp.status_code}): {a['title']}")
        print(f"  {resp.text[:200]}")

print(f"\nDone! {success}/{len(articles)} articles created.")
