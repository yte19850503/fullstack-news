"""
认证模块测试

覆盖：
- 注册：正常注册、重复邮箱
- 登录：正常登录、错误密码、不存在的邮箱
- 登出：正常登出、未登录访问
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from conftest import auth_header


class TestRegister:
    def test_register_success(self, client):
        resp = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@test.com",
                "password": "Test1234",
                "name": "New User",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        assert len(data["token"]) > 20

    def test_register_duplicate_email(self, client, reader):
        resp = client.post(
            "/api/auth/register",
            json={
                "email": "reader@test.com",
                "password": "Test1234",
                "name": "Duplicate",
            },
        )
        assert resp.status_code == 400
        assert "already registered" in resp.json()["detail"]

    def test_register_missing_fields(self, client):
        resp = client.post(
            "/api/auth/register",
            json={
                "email": "incomplete@test.com",
            },
        )
        assert resp.status_code == 422


class TestLogin:
    def test_login_success(self, client, reader):
        resp = client.post(
            "/api/auth/login",
            json={
                "email": "reader@test.com",
                "password": "123456",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data

    def test_login_wrong_password(self, client, reader):
        resp = client.post(
            "/api/auth/login",
            json={
                "email": "reader@test.com",
                "password": "wrongpass",
            },
        )
        assert resp.status_code == 401
        assert "Invalid" in resp.json()["detail"]

    def test_login_nonexistent_email(self, client):
        resp = client.post(
            "/api/auth/login",
            json={
                "email": "nobody@test.com",
                "password": "123456",
            },
        )
        assert resp.status_code == 401


class TestLogout:
    def test_logout_success(self, client, reader):
        resp = client.post("/api/auth/logout", headers=auth_header(reader))
        assert resp.status_code == 200
        assert resp.json()["message"] == "Logged out successfully"

    def test_logout_without_token(self, client):
        resp = client.post("/api/auth/logout")
        assert resp.status_code == 403

    def test_logout_with_invalid_token(self, client):
        resp = client.post(
            "/api/auth/logout",
            headers={
                "Authorization": "Bearer invalid.token.here",
            },
        )
        assert resp.status_code in (401, 403)
