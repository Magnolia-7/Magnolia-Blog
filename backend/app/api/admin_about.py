from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models.about import About
from app.models.admin_user import AdminUser
from app.schemas.about import AboutResponse, AboutUpdate

router = APIRouter(
    prefix="/api/admin/about",
    tags=["Admin About"],
)

@router.get("/", response_model=AboutResponse | None)
def get_about(
    db: Session = Depends(get_db),
    current_admin_user: AdminUser = Depends(get_current_admin)
):
    about = db.query(About).order_by(About.id.asc()).first()
    return about

@router.patch("/", response_model=AboutResponse)
def update_about(
    about_update:AboutUpdate,
    db: Session = Depends(get_db),
    current_admin_user: AdminUser = Depends(get_current_admin)
):
    about = db.query(About).order_by(About.id.asc()).first()

    if not about:
        about = About()
        db.add(about)
        db.flush()

    update_data = about_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(about, field, value)

    db.commit()
    db.refresh(about)

    return about




    