from datetime import datetime

from pydantic import BaseModel


class AdSlotCreate(BaseModel):
    name: str
    position: str
    ad_type: str
    platform: str
    code: str
    weight: int = 1


class AdSlotUpdate(BaseModel):
    name: str | None = None
    position: str | None = None
    ad_type: str | None = None
    platform: str | None = None
    code: str | None = None
    status: str | None = None
    weight: int | None = None


class AdSlotResponse(BaseModel):
    id: int
    name: str
    position: str
    ad_type: str
    platform: str
    code: str
    status: str
    weight: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AdPublicResponse(BaseModel):
    id: int
    name: str
    position: str
    ad_type: str
    code: str

    model_config = {"from_attributes": True}


class AdStatResponse(BaseModel):
    slot_id: int
    date: str
    impressions: int
    clicks: int
