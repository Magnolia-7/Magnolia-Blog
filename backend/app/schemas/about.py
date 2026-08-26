from datetime import datetime
from pydantic import BaseModel, Field

class AboutBase(BaseModel):
    avatar: str | None = None
    nickname: str | None = None
    signature: str | None = None

    bio: str | None = None
    interests: str | None = None 
    skills: str | None = None
    contacts: str | None = None

    mood: str | None = None
    short_goal: str | None = None
    long_goal: str | None = None
    current_song: str | None = None
    current_song_url: str | None = None
    profile_tags: str | None = None
    hero_subtitle: str | None = None
    home_thought: str | None = None

    social_links: str | None = None
    tech_stack: str | None = None

class AboutUpdate(AboutBase):
    pass

class AboutResponse(AboutBase):
    id: int
    updated_at: datetime

    model_config = {"from_attributes": True}
