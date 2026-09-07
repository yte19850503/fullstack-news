from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate
from app.services.comment import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])
comment_service = CommentService()


@router.get("/article/{article_id}", summary="获取文章的评论列表")
def list_comments(article_id: int, db: Session = Depends(get_db)):
    return comment_service.list_by_article(db, article_id)


@router.post("/", summary="发表评论（需登录）")
def create_comment(
    body: CommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return comment_service.create(db, body.content, body.article_id, user.id, body.parent_id)


@router.delete("/{comment_id}", summary="删除评论（作者本人或 ADMIN）")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment_service.delete(db, comment_id, user.id, user.role.value)
    return {"message": "Deleted"}
