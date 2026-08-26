from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.post import Post
from app.schemas.post import PaginatedPostResponse, PostResponse

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"],
)

@router.get("/", response_model=PaginatedPostResponse)
def get_posts(
    category: str | None = Query(None, description="文章分类，life 或 study"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(9, ge=1, le=50, description="每页数量"),
    db: Session = Depends(get_db),
):
    query = db.query(Post).filter(Post.status == "published")

    if category is not None:
        if category not in ["life", "study"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category 必须是 life 或 study",
            )
        query = query.filter(Post.category == category)

    total = query.count()
    total_pages = (total + page_size - 1) // page_size

    posts = (
        query
        .order_by(Post.is_pinned.desc(), Post.published_at.desc(), Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }

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
