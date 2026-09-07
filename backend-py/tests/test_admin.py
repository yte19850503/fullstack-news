"""
后台管理模块测试

覆盖：
- 统计面板
- 用户管理：列表、更新、启用/禁用
- 文章管理：列表、审核、批量更新、详情、删除
- 分类管理：列表、创建、更新、删除
- 标签管理：列表、创建、更新、删除
- 评论管理：列表、删除
- 操作日志
- 权限：READER 被拒绝、EDITOR 部分允许
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from conftest import auth_header


class TestAdminStats:
    def test_stats_as_admin(self, client, admin, article):
        resp = client.get("/api/admin/stats", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert "total_users" in data
        assert "total_articles" in data
        assert data["total_articles"] >= 1

    def test_stats_reader_denied(self, client, reader):
        resp = client.get("/api/admin/stats", headers=auth_header(reader))
        assert resp.status_code == 403

    def test_stats_editor_denied(self, client, editor):
        resp = client.get("/api/admin/stats", headers=auth_header(editor))
        assert resp.status_code == 403


class TestAdminUsers:
    def test_list_users(self, client, admin, reader, editor):
        resp = client.get("/api/admin/users", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 3

    def test_list_users_filter_role(self, client, admin, reader, editor):
        resp = client.get("/api/admin/users?role=READER", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert all(u["role"] == "READER" for u in data["items"])

    def test_update_user(self, client, admin, reader):
        resp = client.put(
            f"/api/admin/users/{reader.id}",
            json={
                "name": "Updated Reader",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Reader"

    def test_toggle_user_active(self, client, admin, reader):
        resp = client.put(
            f"/api/admin/users/{reader.id}/toggle-active",
            json={
                "is_active": False,
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False


class TestAdminArticles:
    def test_list_articles(self, client, admin, article):
        resp = client.get("/api/admin/articles", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 1

    def test_editor_can_list_articles(self, client, editor, article):
        resp = client.get("/api/admin/articles", headers=auth_header(editor))
        assert resp.status_code == 200

    def test_get_article_detail(self, client, admin, article):
        resp = client.get(f"/api/admin/articles/{article.id}", headers=auth_header(admin))
        assert resp.status_code == 200
        assert resp.json()["title"] == "测试文章"

    def test_review_article(self, client, admin, article):
        resp = client.put(f"/api/admin/articles/{article.id}/review?status=ARCHIVED", headers=auth_header(admin))
        assert resp.status_code == 200
        assert resp.json()["status"] == "ARCHIVED"

    def test_batch_update_articles(self, client, admin, article, db_session, editor, category):
        from app.models.article import Article, ArticleStatus

        art2 = Article(
            title="Second",
            slug="second-art",
            content="<p>Second</p>",
            status=ArticleStatus.DRAFT,
            author_id=editor.id,
            category_id=category.id,
        )
        db_session.add(art2)
        db_session.commit()

        resp = client.post(
            f"/api/admin/articles/batch-update?status=PUBLISHED",
            json=[article.id, art2.id],
            headers=auth_header(admin),
        )
        assert resp.status_code == 200

    def test_admin_delete_article(self, client, admin, article):
        resp = client.delete(f"/api/admin/articles/{article.id}", headers=auth_header(admin))
        assert resp.status_code == 200

    def test_editor_cannot_delete_article(self, client, editor, article):
        resp = client.delete(f"/api/admin/articles/{article.id}", headers=auth_header(editor))
        assert resp.status_code == 403

    def test_admin_create_article(self, client, admin, category):
        resp = client.post(
            "/api/admin/articles",
            json={
                "title": "Admin Created",
                "content": "<p>By admin</p>",
                "category_id": category.id,
                "status": "PUBLISHED",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Admin Created"

    def test_admin_update_article(self, client, admin, article):
        resp = client.put(
            f"/api/admin/articles/{article.id}",
            json={
                "title": "Admin Updated",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Admin Updated"


class TestAdminCategories:
    def test_list_categories(self, client, admin, category):
        resp = client.get("/api/admin/categories", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

    def test_create_category(self, client, admin):
        resp = client.post("/api/admin/categories?name=NewCat&description=desc", headers=auth_header(admin))
        assert resp.status_code == 200
        assert resp.json()["name"] == "NewCat"

    def test_update_category(self, client, admin, category):
        resp = client.put(f"/api/admin/categories/{category.id}?name=Renamed", headers=auth_header(admin))
        assert resp.status_code == 200
        assert resp.json()["name"] == "Renamed"

    def test_delete_category(self, client, admin, category):
        resp = client.delete(f"/api/admin/categories/{category.id}", headers=auth_header(admin))
        assert resp.status_code == 200


class TestAdminTags:
    def test_list_tags(self, client, admin, tag):
        resp = client.get("/api/admin/tags", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

    def test_create_tag(self, client, admin):
        resp = client.post(
            "/api/admin/tags",
            json={
                "name": "GPT-4",
                "slug": "gpt-4",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "GPT-4"

    def test_update_tag(self, client, admin, tag):
        resp = client.put(
            f"/api/admin/tags/{tag.id}",
            json={
                "name": "ChatGPT-Plus",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "ChatGPT-Plus"

    def test_delete_tag(self, client, admin, tag):
        resp = client.delete(f"/api/admin/tags/{tag.id}", headers=auth_header(admin))
        assert resp.status_code == 200


class TestAdminComments:
    def test_list_comments(self, client, admin, article, reader, db_session):
        from app.models.comment import Comment

        c = Comment(content="Test comment", article_id=article.id, user_id=reader.id)
        db_session.add(c)
        db_session.commit()

        resp = client.get("/api/admin/comments", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 1

    def test_delete_comment(self, client, admin, article, reader, db_session):
        from app.models.comment import Comment

        c = Comment(content="Delete me", article_id=article.id, user_id=reader.id)
        db_session.add(c)
        db_session.commit()
        db_session.refresh(c)

        resp = client.delete(f"/api/admin/comments/{c.id}", headers=auth_header(admin))
        assert resp.status_code == 200


class TestAdminLogs:
    def test_list_logs(self, client, admin):
        resp = client.get("/api/admin/logs", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data


class TestAdminPermissions:
    def test_reader_denied_everywhere(self, client, reader):
        endpoints = [
            ("GET", "/api/admin/stats"),
            ("GET", "/api/admin/users"),
            ("GET", "/api/admin/articles"),
            ("GET", "/api/admin/categories"),
            ("GET", "/api/admin/tags"),
            ("GET", "/api/admin/comments"),
            ("GET", "/api/admin/logs"),
        ]
        for method, url in endpoints:
            resp = client.request(method, url, headers=auth_header(reader))
            assert resp.status_code == 403, f"{method} {url} should be 403 for READER"

    def test_editor_can_access_articles(self, client, editor, article):
        resp = client.get("/api/admin/articles", headers=auth_header(editor))
        assert resp.status_code == 200

    def test_editor_denied_admin_only(self, client, editor):
        admin_only = [
            ("GET", "/api/admin/stats"),
            ("GET", "/api/admin/users"),
            ("GET", "/api/admin/categories"),
            ("GET", "/api/admin/tags"),
            ("GET", "/api/admin/comments"),
            ("GET", "/api/admin/logs"),
        ]
        for method, url in admin_only:
            resp = client.request(method, url, headers=auth_header(editor))
            assert resp.status_code == 403, f"{method} {url} should be 403 for EDITOR"

    def test_unauthenticated_denied(self, client):
        resp = client.get("/api/admin/stats")
        assert resp.status_code == 403
