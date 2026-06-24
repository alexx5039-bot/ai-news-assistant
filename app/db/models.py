from datetime import datetime

from sqlalchemy import String, Text, DateTime, Enum, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.enums import ArticleStatus, UserRole

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[ArticleStatus] = mapped_column(
        Enum(ArticleStatus),
        default=ArticleStatus.DRAFT,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(),)

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
    sources: Mapped[list["ArticleSource"]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="articles")



class ArticleSource(Base):
    __tablename__ = "article_sources"

    id: Mapped[int] = mapped_column(primary_key=True)

    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id")
    )

    title: Mapped[str] = mapped_column(String(500))

    url: Mapped[str] = mapped_column(String(1000))

    article: Mapped["Article"] = relationship(
        back_populates="sources"
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )
    articles: Mapped[list["Article"]] = relationship(back_populates="author")