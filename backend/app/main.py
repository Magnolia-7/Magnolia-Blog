from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.admin_posts import router as admin_posts_router
from app.api.posts import router as posts_router
from app.api.search import router as search_router
from app.api.about import router as about_router
from app.api.admin_about import router as admin_about_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_posts_router)
app.include_router(posts_router)
app.include_router(search_router)
app.include_router(about_router)
app.include_router(admin_about_router)

@app.get("/")
def read_root():
    return {"message": "Backend API is running"}