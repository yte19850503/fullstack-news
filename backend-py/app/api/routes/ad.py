from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.models.user import User
from app.schemas.ad import AdSlotCreate, AdSlotUpdate
from app.services.ad import ad_service

router = APIRouter(prefix="/ads", tags=["ads"])


@router.get("/public", summary="获取公开广告位（按权重随机）")
def get_public_ads(
    position: str = Query(..., description="广告位位置: header/sidebar/infeed/inarticle/footer"),
    db: Session = Depends(get_db),
):
    return ad_service.get_public_slots(db, position)


@router.post("/public/{slot_id}/event", summary="上报广告事件（impression/click）")
def record_ad_event(
    slot_id: int,
    event: str = Query(..., pattern="^(impression|click)$"),
    request: Request = None,
    db: Session = Depends(get_db),
):
    ip = request.client.host if request else None
    ad_service.record_event(db, slot_id, event, ip)
    return {"message": "Recorded"}


@router.get("/", summary="广告位列表（后台管理）")
def list_ad_slots(
    position: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return ad_service.list_slots(db, position)


@router.post("/", summary="创建广告位")
def create_ad_slot(
    body: AdSlotCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return ad_service.create_slot(db, body.model_dump(), user.id)


@router.put("/{slot_id}", summary="更新广告位")
def update_ad_slot(
    slot_id: int,
    body: AdSlotUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return ad_service.update_slot(db, slot_id, body.model_dump(exclude_unset=True))


@router.delete("/{slot_id}", summary="删除广告位")
def delete_ad_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    ad_service.delete_slot(db, slot_id)
    return {"message": "Deleted"}


@router.get("/stats", summary="广告统计数据")
def get_ad_stats(
    slot_id: int | None = None,
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return ad_service.get_stats(db, slot_id, days)
