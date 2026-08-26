from app.core.database import engine, Base
from app.models import (
    AdminUser,
    Album,
    About,
    ChangelogEntry,
    GuestbookMessage,
    LearningNode,
    LibraryItem,
    MediaAsset,
    Photo,
    Post,
    SocialLink,
    TechStack,
)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
