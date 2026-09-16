from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models.admin_user import AdminUser
from app.models.post import Post
from app.schemas.post import PaginatedPostResponse, PostCreate, PostResponse, PostUpdate

router = APIRouter(
    prefix="/api/admin/posts",
    tags=["Admin Posts"],
)

# 新增文章
@router.post("/", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    if post_data.category not in ["life", "study"]:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="catagory 必须是 life 或 study",
        )
    
    if post_data.status not in ["draft", "published"]:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="status 必须是 draft 或 published",
        )
    
    values = post_data.model_dump()
    values["summary"] = values.get("summary") or ""
    if values["status"] == "published" and not values.get("published_at"):
        values["published_at"] = datetime.now()
    post = Post(**values)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post
# 获取后台文章列表
@router.get("/", response_model=PaginatedPostResponse)
def get_admin_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    category: str | None = Query(default=None, pattern="^(life|study)$"),
    post_status: str | None = Query(default=None, alias="status", pattern="^(draft|published)$"),
    keyword: str | None = Query(default=None, max_length=100),
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    query = db.query(Post)
    if category:
        query = query.filter(Post.category == category)
    if post_status:
        query = query.filter(Post.status == post_status)
    if keyword and keyword.strip():
        pattern = f"%{keyword.strip()}%"
        query = query.filter(or_(
            Post.title.ilike(pattern),
            Post.summary.ilike(pattern),
            Post.tags.ilike(pattern),
        ))

    total = query.count()
    posts = query.order_by(Post.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }
# 后台文章详情
@router.get("/{post_id}", response_model=PostResponse)
def get_admin_post_detail(
    post_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    return post
# 编辑文章
@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    update_date = post_data.model_dump(exclude_unset=True)

    if "category" in update_date and update_date["category"] not in ["life", "study"]:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="catagory 必须是 life 或 study",
        )
    
    if "status" in update_date and update_date["status"] not in ["draft", "published"]:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="status 必须是 draft 或 published",
        )

    if update_date.get("status") == "published" and not post.published_at:
        update_date["published_at"] = datetime.now()
    
    for field, value in update_date.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)

    return post
# 删除文章
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    db.delete(post)
    db.commit()

    return {
        "detail": "文章删除成功",
        "post_id": post_id,
        }
