from datetime import datetime
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    summary: str | None = None
    content: str = Field(..., min_length=1)
    cover_image: str | None = None
    category: str = Field(..., description="life 或 study")
    status: str = Field(default="draft", description="draft 或 published")


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    content: str | None = None
    cover_image: str | None = None
    category: str | None = None
    status: str | None = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }