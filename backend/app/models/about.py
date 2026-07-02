from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)

    avatar = Column(String(255), nullable=True)
    nickname = Column(String(100), nullable=True)
    signature = Column(String(255), nullable=True)

    bio = Column(Text, nullable=True)
    interests = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    contacts = Column(Text, nullable=True)

    mood = Column(String(100), nullable=True)
    short_goal = Column(String(255), nullable=True)
    long_goal = Column(String(255), nullable=True)

    social_links = Column(Text, nullable=True)
    tech_stack = Column(Text, nullable=True)

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )