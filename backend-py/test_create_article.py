import requests, json

# Login
r = requests.post("http://127.0.0.1:8003/api/auth/login", json={"email": "admin@test.com", "password": "admin123"})
print("Login status:", r.status_code)
if r.status_code != 200:
    print("Login failed:", r.text)
    exit(1)

print("Login response:", r.json())
token = r.json()["token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Create article with Chinese title
r = requests.post(
    "http://127.0.0.1:8003/api/admin/articles",
    json={
        "title": "阿里通义万相2.6震撼发布",
        "content": "<p>这是一篇测试文章</p><p>第二段内容</p>",
        "category_id": 1,
        "status": "PUBLISHED",
        "tag_ids": [1],
    },
    headers=headers,
)
data = r.json()
print("Create status:", r.status_code)
slug = data.get("slug", "")
print("Slug:", slug)
print("ID:", data.get("id"))

# Now test: fetch article detail by slug through the FRONTEND PROXY
r2 = requests.get(f"http://127.0.0.1:5174/api/articles/{slug}")
print(f"\nDetail via frontend proxy status: {r2.status_code}")
print("Response:", r2.text[:200] if r2.status_code == 200 else r2.text)

# Also test with URL-encoded slug
import urllib.parse

encoded_slug = urllib.parse.quote(slug)
print(f"\nEncoded slug: {encoded_slug}")
r3 = requests.get(f"http://127.0.0.1:5174/api/articles/{encoded_slug}")
print(f"Detail via encoded slug status: {r3.status_code}")
print("Response:", r3.text[:200] if r3.status_code == 200 else r3.text)

# Test directly against backend
r4 = requests.get(f"http://127.0.0.1:8003/api/articles/{slug}")
print(f"\nDetail via backend directly status: {r4.status_code}")
print("Response:", r4.text[:200] if r4.status_code == 200 else r4.text)
