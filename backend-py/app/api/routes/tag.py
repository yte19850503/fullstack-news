from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.tag import TagResponse
from app.models.tag import Tag

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[TagResponse], summary="获取全部标签")
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).order_by(Tag.id).all()
