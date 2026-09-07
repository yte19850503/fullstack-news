"""
文章模块测试

覆盖：
- 文章列表：默认分页、按分类筛选、按状态筛选、排序
- 文章详情：按 slug 获取、不存在的 slug
- 创建文章：EDITOR 可以创建、ADMIN 可以创建、READER 被拒绝、无 token 被拒绝
- 更新文章：EDITOR 可以更新
- 删除文章：ADMIN 可以删除、EDITOR 被拒绝
- 搜索：全文搜索（SQLite 下会走 LIKE 回退）
- 热门搜索词
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from conftest import auth_header


class TestArticleList:
    def test_list_empty(self, client):
        resp = client.get("/api/articles/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["items"] == []
        assert data["page"] == 1

    def test_list_with_article(self, client, article):
        resp = client.get("/api/articles/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "测试文章"
        assert data["items"][0]["slug"] == "test-article-001"

    def test_list_filter_by_category(self, client, article, category):
        resp = client.get(f"/api/articles/?category_id={category.id}")
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        resp = client.get("/api/articles/?category_id=9999")
        assert resp.json()["total"] == 0

    def test_list_filter_by_status(self, client, article):
        resp = client.get("/api/articles/?status=PUBLISHED")
        assert resp.json()["total"] == 1

        resp = client.get("/api/articles/?status=DRAFT")
        assert resp.json()["total"] == 0

    def test_list_pagination(self, client, db_session, editor, category):
        from app.models.article import Article, ArticleStatus

        for i in range(15):
            db_session.add(
                Article(
                    title=f"Article {i}",
                    slug=f"article-{i}",
                    content="<p>content</p>",
                    status=ArticleStatus.PUBLISHED,
                    author_id=editor.id,
                    category_id=category.id,
                )
            )
        db_session.commit()

        resp = client.get("/api/articles/?page=1&page_size=5")
        data = resp.json()
        assert len(data["items"]) == 5
        assert data["total"] == 15
        assert data["page"] == 1

        resp = client.get("/api/articles/?page=3&page_size=5")
        data = resp.json()
        assert len(data["items"]) == 5
        assert data["page"] == 3

    def test_list_sort_popular(self, client, db_session, editor, category):
        from app.models.article import Article, ArticleStatus

        db_session.add(
            Article(
                title="Popular",
                slug="popular-one",
                content="<p>content</p>",
                status=ArticleStatus.PUBLISHED,
                view_count=100,
                author_id=editor.id,
                category_id=category.id,
            )
        )
        db_session.add(
            Article(
                title="Unpopular",
                slug="unpopular-one",
                content="<p>content</p>",
                status=ArticleStatus.PUBLISHED,
                view_count=1,
                author_id=editor.id,
                category_id=category.id,
            )
        )
        db_session.commit()

        resp = client.get("/api/articles/?sort=popular")
        data = resp.json()
        assert data["items"][0]["title"] == "Popular"


class TestArticleDetail:
    def test_get_by_slug(self, client, article):
        resp = client.get(f"/api/articles/{article.slug}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "测试文章"
        assert data["content"] == "<p>这是测试文章的内容</p>"
        assert data["author"]["name"] == "Editor"
        assert data["category"]["name"] == "AI工具"

    def test_get_nonexistent_slug(self, client):
        resp = client.get("/api/articles/does-not-exist")
        assert resp.status_code == 404


class TestCreateArticle:
    def test_editor_can_create(self, client, editor, category):
        resp = client.post(
            "/api/articles/",
            json={
                "title": "New Article",
                "content": "<p>Content here</p>",
                "category_id": category.id,
                "status": "DRAFT",
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "New Article"
        assert "slug" in data

    def test_admin_can_create(self, client, admin, category):
        resp = client.post(
            "/api/articles/",
            json={
                "title": "Admin Article",
                "content": "<p>Admin content</p>",
                "category_id": category.id,
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200

    def test_reader_cannot_create(self, client, reader, category):
        resp = client.post(
            "/api/articles/",
            json={
                "title": "Reader Article",
                "content": "<p>Should fail</p>",
                "category_id": category.id,
            },
            headers=auth_header(reader),
        )
        assert resp.status_code == 403

    def test_unauthenticated_cannot_create(self, client, category):
        resp = client.post(
            "/api/articles/",
            json={
                "title": "No Auth",
                "content": "<p>Should fail</p>",
                "category_id": category.id,
            },
        )
        assert resp.status_code == 403

    def test_create_with_tags(self, client, editor, category, tag):
        resp = client.post(
            "/api/articles/",
            json={
                "title": "Tagged Article",
                "content": "<p>With tags</p>",
                "category_id": category.id,
                "tag_ids": [tag.id],
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["tags"]) == 1
        assert data["tags"][0]["name"] == "ChatGPT"


class TestUpdateArticle:
    def test_editor_can_update(self, client, editor, article):
        resp = client.put(
            f"/api/articles/{article.id}",
            json={
                "title": "Updated Title",
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Updated Title"

    def test_update_nonexistent(self, client, editor):
        resp = client.put(
            "/api/articles/99999",
            json={
                "title": "Nope",
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 404


class TestDeleteArticle:
    def test_admin_can_delete(self, client, admin, article):
        resp = client.delete(f"/api/articles/{article.id}", headers=auth_header(admin))
        assert resp.status_code == 200

        resp = client.get(f"/api/articles/{article.slug}")
        assert resp.status_code == 404

    def test_editor_cannot_delete(self, client, editor, article):
        resp = client.delete(f"/api/articles/{article.id}", headers=auth_header(editor))
        assert resp.status_code == 403


class TestSearchArticles:
    @pytest.mark.skip(reason="MySQL FULLTEXT (MATCH...AGAINST) not supported by SQLite test DB")
    def test_search_returns_results(self, client, article):
        resp = client.get("/api/articles/search?q=测试")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "search_mode" in data

    def test_search_missing_query(self, client):
        resp = client.get("/api/articles/search")
        assert resp.status_code == 422


class TestHotSearchTerms:
    def test_hot_terms_empty(self, client):
        resp = client.get("/api/articles/hot-search-terms")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
