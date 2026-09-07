"""
评论模块测试

覆盖：
- 获取文章评论列表（空、有评论、嵌套回复）
- 发表评论（需登录、回复评论、文章不存在）
- 删除评论（作者本人、ADMIN、他人评论被拒绝）
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from conftest import auth_header


class TestListComments:
    def test_list_empty(self, client, article):
        resp = client.get(f"/api/comments/article/{article.id}")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_with_comments(self, client, article, reader, db_session):
        from app.models.comment import Comment

        c = Comment(content="Great article!", article_id=article.id, user_id=reader.id)
        db_session.add(c)
        db_session.commit()

        resp = client.get(f"/api/comments/article/{article.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["content"] == "Great article!"
        assert data[0]["user"]["name"] == "Reader"

    def test_list_with_replies(self, client, article, reader, editor, db_session):
        from app.models.comment import Comment

        parent = Comment(content="Parent comment", article_id=article.id, user_id=reader.id)
        db_session.add(parent)
        db_session.flush()

        reply = Comment(content="Reply here", article_id=article.id, user_id=editor.id, parent_id=parent.id)
        db_session.add(reply)
        db_session.commit()

        resp = client.get(f"/api/comments/article/{article.id}")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["content"] == "Parent comment"
        assert len(data[0]["replies"]) == 1
        assert data[0]["replies"][0]["content"] == "Reply here"


class TestCreateComment:
    def test_create_success(self, client, article, reader):
        resp = client.post(
            "/api/comments/",
            json={
                "content": "Nice post!",
                "article_id": article.id,
            },
            headers=auth_header(reader),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["content"] == "Nice post!"
        assert data["article_id"] == article.id

    def test_create_reply(self, client, article, reader, editor, db_session):
        from app.models.comment import Comment

        parent = Comment(content="Parent", article_id=article.id, user_id=reader.id)
        db_session.add(parent)
        db_session.commit()
        db_session.refresh(parent)

        resp = client.post(
            "/api/comments/",
            json={
                "content": "My reply",
                "article_id": article.id,
                "parent_id": parent.id,
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 200
        assert resp.json()["parent_id"] == parent.id

    def test_create_without_login(self, client, article):
        resp = client.post(
            "/api/comments/",
            json={
                "content": "Should fail",
                "article_id": article.id,
            },
        )
        assert resp.status_code == 403

    def test_create_article_not_found(self, client, reader):
        resp = client.post(
            "/api/comments/",
            json={
                "content": "No article",
                "article_id": 99999,
            },
            headers=auth_header(reader),
        )
        assert resp.status_code == 404

    def test_create_parent_not_found(self, client, article, reader):
        resp = client.post(
            "/api/comments/",
            json={
                "content": "Bad parent",
                "article_id": article.id,
                "parent_id": 99999,
            },
            headers=auth_header(reader),
        )
        assert resp.status_code == 404


class TestDeleteComment:
    def test_author_can_delete(self, client, article, reader, db_session):
        from app.models.comment import Comment

        c = Comment(content="To delete", article_id=article.id, user_id=reader.id)
        db_session.add(c)
        db_session.commit()
        db_session.refresh(c)

        resp = client.delete(f"/api/comments/{c.id}", headers=auth_header(reader))
        assert resp.status_code == 200

    def test_admin_can_delete_others_comment(self, client, article, reader, admin, db_session):
        from app.models.comment import Comment

        c = Comment(content="Admin delete", article_id=article.id, user_id=reader.id)
        db_session.add(c)
        db_session.commit()
        db_session.refresh(c)

        resp = client.delete(f"/api/comments/{c.id}", headers=auth_header(admin))
        assert resp.status_code == 200

    def test_other_user_cannot_delete(self, client, article, reader, editor, db_session):
        from app.models.comment import Comment

        c = Comment(content="Reader's comment", article_id=article.id, user_id=reader.id)
        db_session.add(c)
        db_session.commit()
        db_session.refresh(c)

        resp = client.delete(f"/api/comments/{c.id}", headers=auth_header(editor))
        assert resp.status_code == 403

    def test_delete_nonexistent(self, client, reader):
        resp = client.delete("/api/comments/99999", headers=auth_header(reader))
        assert resp.status_code == 404
