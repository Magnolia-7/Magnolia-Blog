from datetime import datetime

from pydantic import BaseModel


class MediaResponse(BaseModel):
    id: int
    storage_provider: str
    object_key: str
    thumbnail_key: str | None
    original_name: str
    mime_type: str
    width: int
    height: int
    size_bytes: int
    url: str
    thumbnail_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
