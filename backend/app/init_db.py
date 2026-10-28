from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.database import engine, Base, SessionLocal
from app.models import (
    AdminUser,
    Album,
    About,
    ChangelogEntry,
    FriendLink,
    GuestbookMessage,
    LearningNode,
    LibraryItem,
    MediaAsset,
    Photo,
    Post,
    Project,
    SocialLink,
    TechStack,
    SiteSettings,
)

def init_db():
    Base.metadata.create_all(bind=engine)
    with SessionLocal.begin() as db:
        if db.get(SiteSettings, 1) is None:
            db.add(SiteSettings(id=1, started_on=datetime.now(ZoneInfo("Asia/Shanghai")).date()))
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
