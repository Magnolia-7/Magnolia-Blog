from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class SocialLinkBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    url: str = Field(..., min_length=1, max_length=500)
    icon: str | None = None
    sort_order: int = 0
    enabled: bool = True


class SocialLinkCreate(SocialLinkBase):
    pass


class SocialLinkUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    icon: str | None = None
    sort_order: int | None = None
    enabled: bool | None = None


class SocialLinkResponse(SocialLinkBase):
    id: int
    model_config = {"from_attributes": True}


class TechStackBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    url: str | None = None
    icon: str | None = None
    level: int = Field(default=3, ge=1, le=5)
    sort_order: int = 0
    enabled: bool = True


class TechStackCreate(TechStackBase):
    pass


class TechStackUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    icon: str | None = None
    level: int | None = Field(default=None, ge=1, le=5)
    sort_order: int | None = None
    enabled: bool | None = None


class TechStackResponse(TechStackBase):
    id: int
    model_config = {"from_attributes": True}


class LearningNodeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    status: Literal["locked", "active", "completed"] = "locked"
    lit_at: datetime | None = None
    sort_order: int = 0
    parent_id: int | None = None


class LearningNodeCreate(LearningNodeBase):
    pass


class LearningNodeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal["locked", "active", "completed"] | None = None
    lit_at: datetime | None = None
    sort_order: int | None = None
    parent_id: int | None = None


class LearningNodeResponse(LearningNodeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class LibraryItemBase(BaseModel):
    item_type: Literal["book", "movie", "anime"]
    title: str = Field(..., min_length=1, max_length=200)
    cover_image: str | None = None
    external_url: str | None = None
    status: Literal["wishlist", "reading", "completed"] = "completed"
    rating: float | None = Field(default=None, ge=0, le=10)
    note: str | None = None
    finished_at: date | None = None
    sort_order: int = 0


class LibraryItemCreate(LibraryItemBase):
    pass


class LibraryItemUpdate(BaseModel):
    item_type: Literal["book", "movie", "anime"] | None = None
    title: str | None = None
    cover_image: str | None = None
    external_url: str | None = None
    status: Literal["wishlist", "reading", "completed"] | None = None
    rating: float | None = Field(default=None, ge=0, le=10)
    note: str | None = None
    finished_at: date | None = None
    sort_order: int | None = None


class LibraryItemResponse(LibraryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class PaginatedLibraryResponse(BaseModel):
    items: list[LibraryItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class PhotoBase(BaseModel):
    media_id: int | None = None
    image_url: str
    thumbnail_url: str | None = None
    caption: str | None = None
    taken_at: date | None = None
    sort_order: int = 0


class PhotoCreate(PhotoBase):
    pass


class PhotoResponse(PhotoBase):
    id: int
    album_id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class AlbumBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    cover_image: str | None = None
    sort_order: int = 0


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cover_image: str | None = None
    sort_order: int | None = None


class AlbumResponse(AlbumBase):
    id: int
    photos: list[PhotoResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class GuestbookCreate(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=80)
    website: str | None = Field(default=None, max_length=500)
    content: str = Field(..., min_length=2, max_length=1000)
    company: str | None = Field(default=None, max_length=1, exclude=True)


class GuestbookUpdate(BaseModel):
    status: Literal["pending", "approved", "hidden"] | None = None
    admin_reply: str | None = None


class GuestbookResponse(BaseModel):
    id: int
    nickname: str
    website: str | None
    content: str
    status: str
    admin_reply: str | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ChangelogBase(BaseModel):
    version: str = Field(..., min_length=1, max_length=40)
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    change_type: Literal["feature", "improvement", "fix"] = "feature"
    status: Literal["draft", "published"] = "draft"
    published_at: datetime | None = None


class ChangelogCreate(ChangelogBase):
    pass


class ChangelogUpdate(BaseModel):
    version: str | None = None
    title: str | None = None
    content: str | None = None
    change_type: Literal["feature", "improvement", "fix"] | None = None
    status: Literal["draft", "published"] | None = None
    published_at: datetime | None = None


class ChangelogResponse(ChangelogBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
