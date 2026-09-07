from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])
category_service = CategoryService()


@router.get("/", summary="获取全部分类")
def list_categories(db: Session = Depends(get_db)):
    return category_service.list(db)


@router.post("/", summary="创建分类（需 ADMIN）")
def create_category(
    body: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return category_service.create(db, body.name, body.description)


@router.put("/{category_id}", summary="更新分类（需 ADMIN）")
def update_category(
    category_id: int,
    body: CategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return category_service.update(db, category_id, body.name, body.description)


@router.delete("/{category_id}", summary="删除分类（需 ADMIN）")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    category_service.delete(db, category_id)
    return {"message": "Deleted"}
