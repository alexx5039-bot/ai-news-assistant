from datetime import datetime

from sqlalchemy import String, Text, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.db.enums import ArticleAStatus

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[ArticleAStatus] = mapped_column(
        Enum(ArticleAStatus),
        default=ArticleAStatus.DRAFT,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(),)

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
