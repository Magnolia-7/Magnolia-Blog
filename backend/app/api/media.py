from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models.admin_user import AdminUser
from app.models.content import Photo
from app.models.media import MediaAsset
from app.models.post import Post
from app.schemas.media import MediaResponse
from app.services.media_service import process_and_store_image
from app.services.storage import get_storage


router = APIRouter(prefix="/api/admin/media", tags=["Admin Media"])


def serialize_media(asset: MediaAsset) -> dict:
    storage = get_storage()
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
    db.commit()
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

    url = get_storage().url_for(asset.object_key)
    used_by_post = db.query(Post).filter(
        (Post.cover_image == url) | (Post.content.contains(url))
    ).first()
    used_by_photo = db.query(Photo).filter(Photo.media_id == media_id).first()
    if used_by_post or used_by_photo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="图片正在被文章或相册使用，不能删除",
        )

    storage = get_storage()
    storage.delete(asset.object_key)
    if asset.thumbnail_key:
        storage.delete(asset.thumbnail_key)
    db.delete(asset)
    db.commit()
    return {"detail": "图片已删除"}
