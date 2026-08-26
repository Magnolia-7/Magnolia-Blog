from collections import defaultdict
from datetime import datetime, timedelta, timezone
from threading import Lock

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.content import (
    Album,
    ChangelogEntry,
    GuestbookMessage,
    LearningNode,
    LibraryItem,
    SocialLink,
    TechStack,
)
from app.schemas.content import (
    AlbumResponse,
    ChangelogResponse,
    GuestbookCreate,
    GuestbookResponse,
    LearningNodeResponse,
    LibraryItemResponse,
    SocialLinkResponse,
    TechStackResponse,
)


router = APIRouter(prefix="/api/content", tags=["Public Content"])
_message_attempts: dict[str, list[datetime]] = defaultdict(list)
_rate_lock = Lock()


@router.get("/social-links", response_model=list[SocialLinkResponse])
def get_social_links(db: Session = Depends(get_db)):
    return db.query(SocialLink).filter(SocialLink.enabled.is_(True)).order_by(
        SocialLink.sort_order, SocialLink.id
    ).all()


@router.get("/tech-stacks", response_model=list[TechStackResponse])
def get_tech_stacks(db: Session = Depends(get_db)):
    return db.query(TechStack).filter(TechStack.enabled.is_(True)).order_by(
        TechStack.sort_order, TechStack.id
    ).all()


@router.get("/learning", response_model=list[LearningNodeResponse])
def get_learning_nodes(db: Session = Depends(get_db)):
    return db.query(LearningNode).order_by(LearningNode.sort_order, LearningNode.id).all()


@router.get("/library", response_model=list[LibraryItemResponse])
def get_library_items(
    item_type: str | None = Query(default=None, pattern="^(book|movie|anime)$"),
    db: Session = Depends(get_db),
):
    query = db.query(LibraryItem)
    if item_type:
        query = query.filter(LibraryItem.item_type == item_type)
    return query.order_by(LibraryItem.sort_order, LibraryItem.id.desc()).all()


@router.get("/albums", response_model=list[AlbumResponse])
def get_albums(db: Session = Depends(get_db)):
    return db.query(Album).order_by(Album.sort_order, Album.id.desc()).all()


@router.get("/guestbook", response_model=list[GuestbookResponse])
def get_guestbook(db: Session = Depends(get_db)):
    return db.query(GuestbookMessage).filter(
        GuestbookMessage.status == "approved"
    ).order_by(GuestbookMessage.created_at.desc()).all()


@router.post("/guestbook", status_code=status.HTTP_201_CREATED)
def create_guestbook_message(
    payload: GuestbookCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    if payload.company:
        return {"detail": "留言已提交，审核后显示"}

    forwarded = request.headers.get("x-forwarded-for", "")
    client_key = forwarded.split(",")[0].strip() or (
        request.client.host if request.client else "unknown"
    )
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=10)
    with _rate_lock:
        recent = [stamp for stamp in _message_attempts[client_key] if stamp > cutoff]
        if len(recent) >= 3:
            raise HTTPException(status_code=429, detail="提交太频繁，请稍后再试")
        recent.append(now)
        _message_attempts[client_key] = recent

    message = GuestbookMessage(
        nickname=payload.nickname.strip(),
        website=(payload.website or "").strip() or None,
        content=payload.content.strip(),
        status="pending",
    )
    db.add(message)
    db.commit()
    return {"detail": "留言已提交，审核后显示"}


@router.get("/changelog", response_model=list[ChangelogResponse])
def get_changelog(db: Session = Depends(get_db)):
    return db.query(ChangelogEntry).filter(
        ChangelogEntry.status == "published"
    ).order_by(
        ChangelogEntry.published_at.desc(), ChangelogEntry.id.desc()
    ).all()
