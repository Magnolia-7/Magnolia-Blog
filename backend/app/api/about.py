from fastapi import Depends, APIRouter 
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.about import About
from app.schemas.about import AboutResponse

router = APIRouter(
    prefix="/api/about",
    tags=["About"],
)

@router.get("/", response_model=AboutResponse)
def get_about(
    db: Session = Depends(get_db)
    ):
    about = db.query(About).order_by(About.id.asc()).first()
    return about


