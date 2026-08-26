from app.core.database import SessionLocal
from app.models import AdminUser
from app.core.security import hash_password
from app.core.config import settings

def create_admin():
    db = SessionLocal()
    try:
        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD

        if not password or len(password) < 12:
            raise RuntimeError("请在 backend/.env 中设置至少 12 位的 ADMIN_PASSWORD")

        existing_user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if existing_user:
            print("Admin user already exists.")
            return
        
        admin = AdminUser(
            username=username,
            password_hash=hash_password(password)
        )
        
        db.add(admin)
        db.commit()
        print("Admin user created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
