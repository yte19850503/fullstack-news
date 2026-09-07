import enum
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Enum,
    Integer,
    DateTime,
    ForeignKey,
    Index,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ArticleStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = (
        Index("ix_articles_status_created", "status", "created_at"),
        Index("ix_articles_category", "category_id"),
        Index("ix_articles_author", "author_id"),
        Index("ix_articles_created", "created_at"),
        Index("ix_ft_title_content", "title", "content", mysql_prefix="FULLTEXT"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(400), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[ArticleStatus] = mapped_column(Enum(ArticleStatus), default=ArticleStatus.DRAFT)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    author: Mapped["User"] = relationship(back_populates="articles")
    category: Mapped["Category"] = relationship(back_populates="articles")
    tags: Mapped[list["ArticleTag"]] = relationship(back_populates="article", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="article", cascade="all, delete-orphan")


class ArticleTag(Base):
    __tablename__ = "article_tags"

    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    article: Mapped["Article"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="articles")
