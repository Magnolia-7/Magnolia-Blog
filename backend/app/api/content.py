from collections import defaultdict
from datetime import datetime, timedelta, timezone
from threading import Lock

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.content import (
    Album,
    FriendLink,
    GuestbookMessage,
    LibraryItem,
    Project,
    SocialLink,
)
from app.schemas.content import (
    AlbumResponse,
    FriendLinkResponse,
    GuestbookCreate,
    GuestbookResponse,
    LibraryItemResponse,
    ProjectResponse,
    SocialLinkResponse,
)


router = APIRouter(prefix="/api/content", tags=["Public Content"])
_message_attempts: dict[str, list[datetime]] = defaultdict(list)
_rate_lock = Lock()


@router.get("/social-links", response_model=list[SocialLinkResponse])
def get_social_links(db: Session = Depends(get_db)):
    return db.query(SocialLink).filter(SocialLink.enabled.is_(True)).order_by(
        SocialLink.sort_order, SocialLink.id
    ).all()



@router.get("/projects", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.enabled.is_(True)).order_by(
        Project.featured.desc(), Project.sort_order, Project.id.desc()
    ).all()


@router.get("/friend-links", response_model=list[FriendLinkResponse])
def get_friend_links(db: Session = Depends(get_db)):
    return db.query(FriendLink).filter(FriendLink.enabled.is_(True)).order_by(
        FriendLink.sort_order, FriendLink.id
    ).all()



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
    label = "愿望" if payload.message_type == "wish" else "留言"
    if payload.company:
        return {"detail": f"{label}已提交，审核后显示"}

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
        message_type=payload.message_type,
        status="pending",
    )
    db.add(message)
    db.commit()
    return {"detail": f"{label}已提交，审核后显示"}
