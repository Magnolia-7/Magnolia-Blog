from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.post import Post
from app.schemas.post import PostResponse

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"],
)

@router.get("/", response_model=list[PostResponse])
def get_posts(
    category: str|None = Query(None, description="文章分类，life 或 study"),
    db: Session = Depends(get_db),
):
    query = db.query(Post).filter(Post.status == "published")

    if category is not None:
        if category not in ["life", "study"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="catagory 必须是 life 或 study", 
            )
        query = query.filter(Post.category == category)

    posts = query.order_by(Post.created_at.desc()).all()

    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post_detail(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id, Post.status == "published")
        .first()
        )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在或未发布",
        )
    return post