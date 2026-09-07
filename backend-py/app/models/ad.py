import enum
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey, Index, func, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AdPosition(str, enum.Enum):
    HEADER = "header"
    SIDEBAR = "sidebar"
    INFEED = "infeed"
    INARTICLE = "inarticle"
    FOOTER = "footer"


class AdType(str, enum.Enum):
    BANNER = "banner"
    INFEED = "infeed"
    NATIVE = "native"


class AdPlatform(str, enum.Enum):
    BAIDU = "baidu"
    PANGLE = "pangle"
    TENCENT = "tencent"
    CUSTOM = "custom"


class AdStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class AdSlot(Base):
    __tablename__ = "ad_slots"
    __table_args__ = (Index("ix_ad_slots_position_status", "position", "status"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    position: Mapped[AdPosition] = mapped_column(String(20), index=True)
    ad_type: Mapped[AdType] = mapped_column(String(20))
    platform: Mapped[AdPlatform] = mapped_column(String(20))
    code: Mapped[str] = mapped_column(Text)
    status: Mapped[AdStatus] = mapped_column(String(20), default=AdStatus.ACTIVE, index=True)
    weight: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class AdStat(Base):
    __tablename__ = "ad_stats"
    __table_args__ = (Index("ix_ad_stats_slot_date", "slot_id", "date"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("ad_slots.id", ondelete="CASCADE"))
    event: Mapped[str] = mapped_column(String(20))
    date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
