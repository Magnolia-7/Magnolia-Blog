from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models.admin_user import AdminUser
from app.models.about import About
from app.models.content import Album, LibraryItem, Photo
from app.models.media import MediaAsset
from app.models.post import Post
from app.schemas.media import MediaResponse
from app.services.media_service import process_and_store_image
from app.services.storage import get_storage


router = APIRouter(prefix="/api/admin/media", tags=["Admin Media"])


def serialize_media(asset: MediaAsset) -> dict:
    storage = get_storage(asset.storage_provider)
    return {
        "id": asset.id,
        "storage_provider": asset.storage_provider,
        "object_key": asset.object_key,
        "thumbnail_key": asset.thumbnail_key,
        "original_name": asset.original_name,
        "mime_type": asset.mime_type,
        "width": asset.width,
        "height": asset.height,
        "size_bytes": asset.size_bytes,
        "url": storage.url_for(asset.object_key),
        "thumbnail_url": storage.url_for(asset.thumbnail_key),
        "created_at": asset.created_at,
    }


@router.post("/images", response_model=MediaResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    storage = get_storage()
    data = await process_and_store_image(file, storage)
    asset = MediaAsset(**data)
    db.add(asset)
    try:
        db.commit()
    except Exception:
        db.rollback()
        for key in (data["object_key"], data["thumbnail_key"]):
            try:
                storage.delete(key)
            except Exception:
                pass
        raise
    db.refresh(asset)
    return serialize_media(asset)


@router.get("", response_model=list[MediaResponse])
def list_media(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    assets = db.query(MediaAsset).order_by(MediaAsset.created_at.desc()).all()
    return [serialize_media(asset) for asset in assets]


@router.delete("/{media_id}")
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    asset = db.query(MediaAsset).filter(MediaAsset.id == media_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="图片不存在")

    storage = get_storage(asset.storage_provider)
    url = storage.url_for(asset.object_key)
    thumbnail_url = storage.url_for(asset.thumbnail_key)
    asset_urls = [item for item in (url, thumbnail_url) if item]
    used_by_post = db.query(Post).filter(
        or_(
            Post.cover_image.in_(asset_urls),
            *(Post.content.contains(item) for item in asset_urls),
        )
    ).first()
    used_by_photo = db.query(Photo).filter(
        or_(
            Photo.media_id == media_id,
            Photo.image_url.in_(asset_urls),
            Photo.thumbnail_url.in_(asset_urls),
        )
    ).first()
    used_by_library = db.query(LibraryItem).filter(
        LibraryItem.cover_image.in_(asset_urls)
    ).first()
    used_by_album = db.query(Album).filter(Album.cover_image.in_(asset_urls)).first()
    used_by_about = db.query(About).filter(About.avatar.in_(asset_urls)).first()
    if any((used_by_post, used_by_photo, used_by_library, used_by_album, used_by_about)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="图片正在被网站内容使用，不能删除",
        )

    storage.delete(asset.object_key)
    if asset.thumbnail_key:
        storage.delete(asset.thumbnail_key)
    db.delete(asset)
    db.commit()
    return {"detail": "图片已删除"}
