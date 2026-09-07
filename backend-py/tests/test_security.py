"""
安全测试：SQL 注入、XSS、认证绕过、密码强度
"""

import pytest
from fastapi.testclient import TestClient

from conftest import auth_header


class TestSQLInjection:
    def test_list_sql_injection_in_query(self, client: TestClient, article):
        malicious = "' OR '1'='1"
        resp = client.get("/api/articles/", params={"q": malicious})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0

    def test_list_sql_injection_union(self, client: TestClient, article):
        malicious = "' UNION SELECT * FROM users --"
        resp = client.get("/api/articles/", params={"q": malicious})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0

    def test_article_list_sql_injection_in_category(self, client: TestClient):
        resp = client.get("/api/articles/", params={"category_id": "1 OR 1=1"})
        assert resp.status_code == 422

    def test_article_list_sql_injection_in_status(self, client: TestClient):
        resp = client.get("/api/articles/", params={"status": "PUBLISHED' OR '1'='1"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0


class TestXSS:
    def test_comment_xss_script_tag(self, client: TestClient, article, reader):
        malicious = "<script>alert('xss')</script>"
        resp = client.post(
            "/api/comments/",
            json={"content": malicious, "article_id": article.id},
            headers=auth_header(reader),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "<script>" not in data["content"]
        assert "&lt;script&gt;" in data["content"]

    def test_comment_xss_img_onerror(self, client: TestClient, article, reader):
        malicious = '<img src=x onerror="alert(1)">'
        resp = client.post(
            "/api/comments/",
            json={"content": malicious, "article_id": article.id},
            headers=auth_header(reader),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "<img" not in data["content"]
        assert "&lt;img" in data["content"]

    def test_article_xss_in_title(self, client: TestClient, category, editor):
        malicious = "<script>alert('xss')</script>测试标题"
        resp = client.post(
            "/api/articles/",
            json={
                "title": malicious,
                "content": "正常内容",
                "category_id": category.id,
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "<script>" not in data["title"]

    def test_article_xss_in_content(self, client: TestClient, category, editor):
        malicious = '<p>正常内容</p><script>alert("xss")</script>'
        resp = client.post(
            "/api/articles/",
            json={
                "title": "测试标题",
                "content": malicious,
                "category_id": category.id,
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "<script>" not in data["content"]


class TestAuthenticationBypass:
    def test_access_admin_without_token(self, client: TestClient):
        resp = client.get("/api/admin/stats")
        assert resp.status_code in (401, 403)

    def test_access_admin_with_invalid_token(self, client: TestClient):
        resp = client.get(
            "/api/admin/stats",
            headers={"Authorization": "Bearer invalid_token_here"},
        )
        assert resp.status_code == 401

    def test_create_article_as_reader(self, client: TestClient, category, reader):
        resp = client.post(
            "/api/articles/",
            json={
                "title": "测试",
                "content": "内容",
                "category_id": category.id,
            },
            headers=auth_header(reader),
        )
        assert resp.status_code == 403

    def test_delete_article_as_editor(self, client: TestClient, article, editor):
        resp = client.delete(
            f"/api/articles/{article.id}",
            headers=auth_header(editor),
        )
        assert resp.status_code == 403

    def test_access_admin_stats_as_editor(self, client: TestClient, editor):
        resp = client.get("/api/admin/stats", headers=auth_header(editor))
        assert resp.status_code == 403


class TestPasswordStrength:
    def test_register_weak_password_no_digit(self, client: TestClient):
        resp = client.post(
            "/api/auth/register",
            json={"email": "weak@test.com", "password": "weakpassword", "name": "Weak"},
        )
        assert resp.status_code == 400
        assert "数字" in resp.json()["detail"]

    def test_register_weak_password_no_letter(self, client: TestClient):
        resp = client.post(
            "/api/auth/register",
            json={"email": "weak@test.com", "password": "12345678", "name": "Weak"},
        )
        assert resp.status_code == 400
        assert "字母" in resp.json()["detail"]

    def test_register_weak_password_too_short(self, client: TestClient):
        resp = client.post(
            "/api/auth/register",
            json={"email": "weak@test.com", "password": "abc12", "name": "Weak"},
        )
        assert resp.status_code == 400
        assert "8" in resp.json()["detail"]

    def test_register_strong_password(self, client: TestClient):
        resp = client.post(
            "/api/auth/register",
            json={"email": "strong@test.com", "password": "StrongPass123", "name": "Strong"},
        )
        assert resp.status_code == 200
        assert "token" in resp.json()


class TestSecurityHeaders:
    def test_security_headers_present(self, client: TestClient):
        resp = client.get("/api/health")
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert resp.headers.get("X-Frame-Options") == "DENY"
        assert resp.headers.get("X-XSS-Protection") == "1; mode=block"
        assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_cors_rejects_unauthorized_origin(self, client: TestClient):
        resp = client.options(
            "/api/health",
            headers={"Origin": "http://evil.com"},
        )
        assert "evil.com" not in resp.headers.get("access-control-allow-origin", "")
