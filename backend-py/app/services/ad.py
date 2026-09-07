from __future__ import annotations

import random
from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ad import AdSlot, AdStat, AdStatus
from app.core.exceptions import AppError


class AdService:
    def list_slots(self, db: Session, position: str | None = None) -> list[AdSlot]:
        query = db.query(AdSlot)
        if position:
            query = query.filter(AdSlot.position == position)
        return query.order_by(AdSlot.weight.desc()).all()

    def create_slot(self, db: Session, data: dict, operator_id: int) -> dict:
        slot = AdSlot(**data)
        db.add(slot)
        db.commit()
        db.refresh(slot)
        return {"id": slot.id, "name": slot.name, "position": slot.position}

    def update_slot(self, db: Session, slot_id: int, data: dict) -> dict:
        slot = db.query(AdSlot).filter(AdSlot.id == slot_id).first()
        if not slot:
            raise AppError("Ad slot not found", 404)
        for k, v in data.items():
            setattr(slot, k, v)
        db.commit()
        db.refresh(slot)
        return {"id": slot.id, "name": slot.name, "status": slot.status}

    def delete_slot(self, db: Session, slot_id: int) -> None:
        slot = db.query(AdSlot).filter(AdSlot.id == slot_id).first()
        if not slot:
            raise AppError("Ad slot not found", 404)
        db.delete(slot)
        db.commit()

    def get_public_slots(self, db: Session, position: str) -> list[dict]:
        slots = db.query(AdSlot).filter(AdSlot.position == position, AdSlot.status == AdStatus.ACTIVE).all()
        if not slots:
            return []
        weights = [s.weight for s in slots]
        total = sum(weights)
        chosen = random.choices(slots, weights=[w / total for w in weights], k=1)[0]
        return [
            {
                "id": chosen.id,
                "name": chosen.name,
                "position": chosen.position,
                "ad_type": chosen.ad_type,
                "code": chosen.code,
            }
        ]

    def record_event(self, db: Session, slot_id: int, event: str, ip: str | None) -> None:
        slot = db.query(AdSlot).filter(AdSlot.id == slot_id).first()
        if not slot:
            raise AppError("Ad slot not found", 404)
        stat = AdStat(slot_id=slot_id, event=event, ip=ip)
        db.add(stat)
        db.commit()

    def get_stats(
        self,
        db: Session,
        slot_id: int | None = None,
        days: int = 7,
    ) -> list[dict]:
        cutoff = datetime.now() - timedelta(days=days)
        query = db.query(
            AdStat.slot_id,
            func.date(AdStat.date).label("date"),
            AdStat.event,
            func.count().label("count"),
        ).filter(AdStat.date >= cutoff)
        if slot_id:
            query = query.filter(AdStat.slot_id == slot_id)
        rows = query.group_by(AdStat.slot_id, func.date(AdStat.date), AdStat.event).all()

        result: dict[tuple, dict] = {}
        for r in rows:
            key = (r.slot_id, str(r.date))
            if key not in result:
                result[key] = {"slot_id": r.slot_id, "date": str(r.date), "impressions": 0, "clicks": 0}
            if r.event == "impression":
                result[key]["impressions"] = r.count
            elif r.event == "click":
                result[key]["clicks"] = r.count
        return list(result.values())


ad_service = AdService()
