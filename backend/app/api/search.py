from datetime import date, datetime, time

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.post import Post
from app.schemas.post import PostResponse

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)

@router.get("/", response_model=list[PostResponse])
def search_posts(
    q: str | None = Query(default=None, description="关键词"),
    category: str | None = Query(default=None, pattern="^(life|study)$"),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Post).filter(Post.status == "published")
    if q and q.strip():
        keyword = f"%{q.strip()}%"
        query = query.filter(or_(
            Post.title.ilike(keyword),
            Post.summary.ilike(keyword),
            Post.content.ilike(keyword),
            Post.tags.ilike(keyword),
        ))
    if category:
        query = query.filter(Post.category == category)
    if start_date:
        query = query.filter(Post.created_at >= datetime.combine(start_date, time.min))
    if end_date:
        query = query.filter(Post.created_at <= datetime.combine(end_date, time.max))

    posts = query.order_by(Post.created_at.desc()).limit(100).all()

    return posts
    
