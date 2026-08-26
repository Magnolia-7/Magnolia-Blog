from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models.admin_user import AdminUser
from app.models.content import (
    Album,
    ChangelogEntry,
    GuestbookMessage,
    LearningNode,
    LibraryItem,
    Photo,
    SocialLink,
    TechStack,
)
from app.schemas.content import (
    AlbumCreate,
    AlbumResponse,
    AlbumUpdate,
    ChangelogCreate,
    ChangelogResponse,
    ChangelogUpdate,
    GuestbookResponse,
    GuestbookUpdate,
    LearningNodeCreate,
    LearningNodeResponse,
    LearningNodeUpdate,
    LibraryItemCreate,
    LibraryItemResponse,
    LibraryItemUpdate,
    PhotoCreate,
    PhotoResponse,
    SocialLinkCreate,
    SocialLinkResponse,
    SocialLinkUpdate,
    TechStackCreate,
    TechStackResponse,
    TechStackUpdate,
)


router = APIRouter(prefix="/api/admin/content", tags=["Admin Content"])


def _get_or_404(db: Session, model, item_id: int):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="内容不存在")
    return item


def _update(db: Session, item, payload):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def _delete(db: Session, model, item_id: int):
    item = _get_or_404(db, model, item_id)
    db.delete(item)
    db.commit()
    return {"detail": "内容已删除"}


@router.get("/social-links", response_model=list[SocialLinkResponse])
def list_social_links(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return db.query(SocialLink).order_by(SocialLink.sort_order, SocialLink.id).all()


@router.post("/social-links", response_model=SocialLinkResponse)
def create_social_link(payload: SocialLinkCreate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    item = SocialLink(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item


@router.patch("/social-links/{item_id}", response_model=SocialLinkResponse)
def update_social_link(item_id: int, payload: SocialLinkUpdate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _update(db, _get_or_404(db, SocialLink, item_id), payload)


@router.delete("/social-links/{item_id}")
def delete_social_link(item_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, SocialLink, item_id)


@router.get("/tech-stacks", response_model=list[TechStackResponse])
def list_tech_stacks(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return db.query(TechStack).order_by(TechStack.sort_order, TechStack.id).all()


@router.post("/tech-stacks", response_model=TechStackResponse)
def create_tech_stack(payload: TechStackCreate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    item = TechStack(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item


@router.patch("/tech-stacks/{item_id}", response_model=TechStackResponse)
def update_tech_stack(item_id: int, payload: TechStackUpdate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _update(db, _get_or_404(db, TechStack, item_id), payload)


@router.delete("/tech-stacks/{item_id}")
def delete_tech_stack(item_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, TechStack, item_id)


@router.get("/learning", response_model=list[LearningNodeResponse])
def list_learning(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return db.query(LearningNode).order_by(LearningNode.sort_order, LearningNode.id).all()


@router.post("/learning", response_model=LearningNodeResponse)
def create_learning(payload: LearningNodeCreate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    item = LearningNode(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item


@router.patch("/learning/{item_id}", response_model=LearningNodeResponse)
def update_learning(item_id: int, payload: LearningNodeUpdate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _update(db, _get_or_404(db, LearningNode, item_id), payload)


@router.delete("/learning/{item_id}")
def delete_learning(item_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, LearningNode, item_id)


@router.get("/library", response_model=list[LibraryItemResponse])
def list_library(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return db.query(LibraryItem).order_by(LibraryItem.sort_order, LibraryItem.id.desc()).all()


@router.post("/library", response_model=LibraryItemResponse)
def create_library(payload: LibraryItemCreate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    if payload.item_type not in {"book", "movie", "anime"}: raise HTTPException(400, "类型无效")
    item = LibraryItem(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item


@router.patch("/library/{item_id}", response_model=LibraryItemResponse)
def update_library(item_id: int, payload: LibraryItemUpdate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _update(db, _get_or_404(db, LibraryItem, item_id), payload)


@router.delete("/library/{item_id}")
def delete_library(item_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, LibraryItem, item_id)


@router.get("/albums", response_model=list[AlbumResponse])
def list_albums(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return db.query(Album).order_by(Album.sort_order, Album.id.desc()).all()


@router.post("/albums", response_model=AlbumResponse)
def create_album(payload: AlbumCreate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    item = Album(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item


@router.patch("/albums/{item_id}", response_model=AlbumResponse)
def update_album(item_id: int, payload: AlbumUpdate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _update(db, _get_or_404(db, Album, item_id), payload)


@router.delete("/albums/{item_id}")
def delete_album(item_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, Album, item_id)


@router.post("/albums/{album_id}/photos", response_model=PhotoResponse)
def create_photo(album_id: int, payload: PhotoCreate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    _get_or_404(db, Album, album_id)
    photo = Photo(album_id=album_id, **payload.model_dump()); db.add(photo); db.commit(); db.refresh(photo); return photo


@router.delete("/photos/{photo_id}")
def delete_photo(photo_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, Photo, photo_id)


@router.get("/guestbook", response_model=list[GuestbookResponse])
def list_guestbook(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return db.query(GuestbookMessage).order_by(GuestbookMessage.created_at.desc()).all()


@router.patch("/guestbook/{item_id}", response_model=GuestbookResponse)
def update_guestbook(item_id: int, payload: GuestbookUpdate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _update(db, _get_or_404(db, GuestbookMessage, item_id), payload)


@router.delete("/guestbook/{item_id}")
def delete_guestbook(item_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, GuestbookMessage, item_id)


@router.get("/changelog", response_model=list[ChangelogResponse])
def list_changelog(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return db.query(ChangelogEntry).order_by(ChangelogEntry.created_at.desc()).all()


@router.post("/changelog", response_model=ChangelogResponse)
def create_changelog(payload: ChangelogCreate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    item = ChangelogEntry(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item


@router.patch("/changelog/{item_id}", response_model=ChangelogResponse)
def update_changelog(item_id: int, payload: ChangelogUpdate, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _update(db, _get_or_404(db, ChangelogEntry, item_id), payload)


@router.delete("/changelog/{item_id}")
def delete_changelog(item_id: int, db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    return _delete(db, ChangelogEntry, item_id)
