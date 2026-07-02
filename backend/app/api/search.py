from fastapi import APIRouter, Depends, HTTPException, status, Query
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
    q: str = Query(..., min_length=1, description="关键词"),
    db: Session = Depends(get_db),
):
    keyword = f"%{q}%"

    posts = (
        db.query(Post)
        .filter(
            Post.status == "published",
            or_(
                Post.title.ilike(keyword),
                Post.summary.ilike(keyword),
                Post.content.ilike(keyword),
            )
    ).order_by(Post.created_at.desc())
    .all()
    )

    return posts
    
