"""
分类 + 标签模块测试

覆盖：
- 分类：公开列表、ADMIN 创建/更新/删除、非 ADMIN 被拒绝
- 标签：公开列表（无需认证）
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from conftest import auth_header


class TestCategoryPublic:
    def test_list_categories_empty(self, client):
        resp = client.get("/api/categories/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_categories_with_data(self, client, category):
        resp = client.get("/api/categories/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "AI工具"
        assert data[0]["slug"] == "ai-tools"


class TestCategoryAdmin:
    def test_admin_create_category(self, client, admin):
        resp = client.post(
            "/api/categories/",
            json={
                "name": "新分类",
                "description": "描述信息",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "新分类"
        assert "slug" in data

    def test_editor_cannot_create_category(self, client, editor):
        resp = client.post(
            "/api/categories/",
            json={
                "name": "Should Fail",
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 403

    def test_admin_update_category(self, client, admin, category):
        resp = client.put(
            f"/api/categories/{category.id}",
            json={
                "name": "改名了",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "改名了"

    def test_admin_delete_category(self, client, admin, category):
        resp = client.delete(f"/api/categories/{category.id}", headers=auth_header(admin))
        assert resp.status_code == 200

        resp = client.get("/api/categories/")
        assert resp.json() == []


class TestTags:
    def test_list_tags_empty(self, client):
        resp = client.get("/api/tags/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_tags_with_data(self, client, tag):
        resp = client.get("/api/tags/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "ChatGPT"
        assert data[0]["slug"] == "chatgpt"

    def test_tags_no_auth_required(self, client, tag):
        resp = client.get("/api/tags/")
        assert resp.status_code == 200
