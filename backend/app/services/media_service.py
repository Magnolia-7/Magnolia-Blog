import asyncio
from datetime import datetime
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageOps, UnidentifiedImageError

from app.core.config import settings
from app.services.storage import StorageBackend


# Pillow may identify some valid iPhone JPEG files as MPO because they contain
# an MPF/multi-picture index. The primary frame is still safe to process just
# like a regular JPEG.
ALLOWED_FORMATS = {"JPEG", "MPO", "PNG", "WEBP"}


def _encode_webp(image: Image.Image, max_edge: int, quality: int) -> tuple[bytes, int, int]:
    result = ImageOps.exif_transpose(image).convert("RGB")
    result.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    result.save(buffer, format="WEBP", quality=quality, method=6)
    return buffer.getvalue(), result.width, result.height


async def process_and_store_image(
    upload: UploadFile,
    storage: StorageBackend,
) -> dict:
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    raw = await upload.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"图片不能超过 {settings.MAX_UPLOAD_SIZE_MB} MB",
        )

    original_name = Path(upload.filename or "image").name[:255]
    return await asyncio.to_thread(
        _process_and_store_image_bytes,
        raw,
        original_name,
        storage,
    )


def _process_and_store_image_bytes(
    raw: bytes,
    original_name: str,
    storage: StorageBackend,
) -> dict:

    try:
        image = Image.open(BytesIO(raw))
        image.verify()
        image = Image.open(BytesIO(raw))
    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持有效的 JPEG、PNG 或 WebP 图片",
        )

    if image.format not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持 JPEG、PNG 或 WebP 图片",
        )

    full_bytes, width, height = _encode_webp(image, max_edge=2560, quality=84)
    thumb_bytes, _, _ = _encode_webp(image, max_edge=640, quality=78)

    now = datetime.now()
    stem = uuid4().hex
    prefix = f"{now:%Y/%m}"
    object_key = f"{prefix}/{stem}.webp"
    thumbnail_key = f"{prefix}/{stem}-thumb.webp"

    stored = storage.put(object_key, full_bytes, content_type="image/webp")
    try:
        storage.put(thumbnail_key, thumb_bytes, content_type="image/webp")
    except Exception:
        try:
            storage.delete(object_key)
        except Exception:
            pass
        raise

    return {
        "storage_provider": storage.provider,
        "object_key": object_key,
        "thumbnail_key": thumbnail_key,
        "original_name": original_name,
        "mime_type": "image/webp",
        "width": width,
        "height": height,
        "size_bytes": stored.size_bytes,
    }
