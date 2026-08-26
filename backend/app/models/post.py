from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, Text
from app.core.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    summary = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    cover_image = Column(String(500), nullable=True)
    category = Column(String(20), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="draft", index=True)
    tags = Column(String(500), nullable=True)
    is_pinned = Column(Boolean, nullable=False, default=False, index=True)
    published_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
        )
