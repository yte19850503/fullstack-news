from sqlalchemy.orm import Session, joinedload

from app.models.comment import Comment
from app.models.article import Article
from app.core.exceptions import AppError
from app.core.sanitizer import sanitize_text


class CommentService:
    def list_by_article(self, db: Session, article_id: int) -> list[dict]:
        comments = (
            db.query(Comment)
            .options(joinedload(Comment.user), joinedload(Comment.replies).joinedload(Comment.user))
            .filter(Comment.article_id == article_id, Comment.parent_id.is_(None))
            .order_by(Comment.created_at.desc())
            .limit(20)
            .all()
        )
        seen = set()
        result = []
        for c in comments:
            if c.id not in seen:
                seen.add(c.id)
                result.append(self._to_dict(c))
        return result

    def create(self, db: Session, content: str, article_id: int, user_id: int, parent_id: int | None = None) -> dict:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise AppError("Article not found", 404)

        if parent_id:
            parent = db.query(Comment).filter(Comment.id == parent_id).first()
            if not parent:
                raise AppError("Parent comment not found", 404)

        clean_content = sanitize_text(content) or content
        comment = Comment(content=clean_content, article_id=article_id, user_id=user_id, parent_id=parent_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return self._to_dict(comment)

    def delete(self, db: Session, comment_id: int, user_id: int, user_role: str) -> None:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise AppError("Comment not found", 404)
        if comment.user_id != user_id and user_role != "ADMIN":
            raise AppError("Insufficient permissions", 403)
        db.delete(comment)
        db.commit()

    def _to_dict(self, comment: Comment) -> dict:
        return {
            "id": comment.id,
            "content": comment.content,
            "article_id": comment.article_id,
            "user_id": comment.user_id,
            "parent_id": comment.parent_id,
            "created_at": comment.created_at.isoformat() if comment.created_at else None,
            "user": {
                "id": comment.user.id,
                "name": comment.user.name,
                "avatar": comment.user.avatar,
            }
            if comment.user
            else None,
            "replies": [self._to_dict(r) for r in comment.replies],
        }
