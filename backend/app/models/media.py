from sqlalchemy import Column, DateTime, Integer, String, func

from app.core.database import Base


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(Integer, primary_key=True, index=True)
    storage_provider = Column(String(20), nullable=False, default="local", index=True)
    object_key = Column(String(500), nullable=False, unique=True)
    thumbnail_key = Column(String(500), nullable=True)
    original_name = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
