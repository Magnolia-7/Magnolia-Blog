from datetime import datetime
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    summary: str | None = None
    content: str = Field(..., min_length=1)
    cover_image: str | None = None
    category: str = Field(..., description="life 或 study")
    status: str = Field(default="draft", description="draft 或 published")
    tags: str | None = None
    is_pinned: bool = False
    published_at: datetime | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    content: str | None = None
    cover_image: str | None = None
    category: str | None = None
    status: str | None = None
    tags: str | None = None
    is_pinned: bool | None = None
    published_at: datetime | None = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class PaginatedPostResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
