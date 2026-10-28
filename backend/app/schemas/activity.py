from datetime import date
from typing import Literal
from urllib.parse import urlparse
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class TimeEntry(BaseModel):
    category: str = Field(min_length=1, max_length=80)
    minutes: int = Field(ge=1, le=1440, strict=True)

    @field_validator("category")
    @classmethod
    def clean_category(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("项目名称不能为空")
        return value


class DailyTimeLogWrite(BaseModel):
    entries: list[TimeEntry] = Field(default_factory=list, max_length=30)

    @model_validator(mode="after")
    def validate_entries(self):
        names = [entry.category for entry in self.entries]
        if len(names) != len(set(names)):
            raise ValueError("同一天的投入项目不能重复")
        if sum(entry.minutes for entry in self.entries) > 1440:
            raise ValueError("每日总投入不能超过 24 小时")
        return self


class DailyTimeLogResponse(DailyTimeLogWrite):
    date: date
    total_minutes: int


class TimeSummaryItem(BaseModel):
    category: str
    minutes: int
    days: int


class TimeSummaryResponse(BaseModel):
    total_minutes: int
    tracked_days: int
    start_date: date | None
    end_date: date
    categories: list[TimeSummaryItem]


class SiteSettingsWrite(BaseModel):
    started_on: date
    avatar_url: str | None = Field(default=None, max_length=500)
    hero_image_url: str | None = Field(default=None, max_length=500)

    @field_validator("avatar_url", "hero_image_url")
    @classmethod
    def validate_image(cls, value):
        value = (value or "").strip()
        if not value:
            return None
        if value.startswith("/") and not value.startswith("//") and "\\" not in value:
            return value
        parsed = urlparse(value)
        if parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise ValueError("图片地址须为站内路径或 http/https 链接")
        return value


class SiteSettingsResponse(SiteSettingsWrite):
    model_config = {"from_attributes": True}


class SiteStatsResponse(BaseModel):
    visitors: int
    page_views: int
    articles: int
    started_on: date
    running_days: int


class VisitCreate(BaseModel):
    visitor_id: UUID
    event_id: UUID
    path: str = Field(min_length=1, max_length=200)

    @field_validator("path")
    @classmethod
    def public_path(cls, value):
        value = value.split("?", 1)[0].split("#", 1)[0]
        if not value.startswith("/") or value.startswith("//"):
            raise ValueError("访问路径无效")
        if value.startswith(("/admin", "/login", "/api")):
            raise ValueError("此页面不计入访客统计")
        return value
