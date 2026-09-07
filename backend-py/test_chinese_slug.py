import requests, json, urllib.parse

# Create article directly via backend service to get proper slug
import sys, os

sys.path.insert(0, ".")
os.environ.setdefault("APP_ENV", "development")

from app.database import SessionLocal
from app.models.article import Article, ArticleStatus
from app.services.article import _to_slug

db = SessionLocal()

# Create a test article with Chinese title
title = "阿里通义万相2.6震撼发布"
slug = _to_slug(title)
print(f"Generated slug: {slug}")
print(f"Slug repr: {repr(slug)}")

article = Article(
    title=title,
    slug=slug,
    content="<p>这是一篇测试文章的内容</p><p>第二段内容</p>",
    summary="测试摘要",
    status=ArticleStatus.PUBLISHED,
    author_id=1,
    category_id=1,
)
db.add(article)
db.commit()
db.refresh(article)
print(f"Created article id={article.id}, slug={article.slug}")
db.close()

# Test 1: fetch directly from backend
print(f"\n--- Test 1: Direct backend fetch ---")
r = requests.get(f"http://127.0.0.1:8003/api/articles/{slug}")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Title: {r.json().get('title')}")
else:
    print(f"Error: {r.text}")

# Test 2: fetch through frontend proxy
print(f"\n--- Test 2: Frontend proxy fetch ---")
r = requests.get(f"http://127.0.0.1:5174/api/articles/{slug}")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Title: {r.json().get('title')}")
else:
    print(f"Error: {r.text}")

# Test 3: fetch with URL-encoded slug through frontend proxy
encoded = urllib.parse.quote(slug)
print(f"\n--- Test 3: Frontend proxy with encoded slug ---")
print(f"Encoded slug: {encoded}")
r = requests.get(f"http://127.0.0.1:5174/api/articles/{encoded}")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Title: {r.json().get('title')}")
else:
    print(f"Error: {r.text}")

# Test 4: double-encoded slug (simulating what might happen in browser)
double_encoded = urllib.parse.quote(encoded)
print(f"\n--- Test 4: Double-encoded slug ---")
print(f"Double-encoded: {double_encoded}")
r = requests.get(f"http://127.0.0.1:5174/api/articles/{double_encoded}")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Title: {r.json().get('title')}")
else:
    print(f"Error: {r.text}")
