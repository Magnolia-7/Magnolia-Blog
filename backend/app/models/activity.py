from sqlalchemy import Column, Date, DateTime, Integer, JSON, String, func

from app.core.database import Base


class DailyTimeLog(Base):
    __tablename__ = "daily_time_logs"

    date = Column(Date, primary_key=True)
    entries = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True)
    started_on = Column(Date, nullable=False)
    avatar_url = Column(String(500), nullable=True)
    hero_image_url = Column(String(500), nullable=True)


class SiteVisit(Base):
    __tablename__ = "site_visits"

    event_id = Column(String(36), primary_key=True)
    visitor_hash = Column(String(64), nullable=False, index=True)
    path = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
