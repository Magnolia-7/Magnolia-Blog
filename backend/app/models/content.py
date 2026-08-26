from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class SocialLink(Base):
    __tablename__ = "social_links"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    url = Column(String(500), nullable=False)
    icon = Column(String(80), nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)
    enabled = Column(Boolean, nullable=False, default=True)


class TechStack(Base):
    __tablename__ = "tech_stacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    url = Column(String(500), nullable=True)
    icon = Column(String(80), nullable=True)
    level = Column(Integer, nullable=False, default=3)
    sort_order = Column(Integer, nullable=False, default=0)
    enabled = Column(Boolean, nullable=False, default=True)


class LearningNode(Base):
    __tablename__ = "learning_nodes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="locked", index=True)
    lit_at = Column(DateTime, nullable=True)
    sort_order = Column(Integer, nullable=False, default=0, index=True)
    parent_id = Column(Integer, ForeignKey("learning_nodes.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class LibraryItem(Base):
    __tablename__ = "library_items"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String(20), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    cover_image = Column(String(500), nullable=True)
    external_url = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="completed", index=True)
    rating = Column(Float, nullable=True)
    note = Column(Text, nullable=True)
    finished_at = Column(Date, nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    cover_image = Column(String(500), nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    photos = relationship(
        "Photo",
        back_populates="album",
        cascade="all, delete-orphan",
        order_by="Photo.sort_order, Photo.id",
    )


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), nullable=False, index=True)
    media_id = Column(Integer, ForeignKey("media_assets.id", ondelete="SET NULL"), nullable=True)
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    caption = Column(String(500), nullable=True)
    taken_at = Column(Date, nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    album = relationship("Album", back_populates="photos")


class GuestbookMessage(Base):
    __tablename__ = "guestbook_messages"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(80), nullable=False)
    website = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    admin_reply = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class ChangelogEntry(Base):
    __tablename__ = "changelog_entries"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(40), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    change_type = Column(String(20), nullable=False, default="feature")
    status = Column(String(20), nullable=False, default="draft", index=True)
    published_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
