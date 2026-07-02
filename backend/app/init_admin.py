from app.core.database import SessionLocal
from app.models import AdminUser
from app.core.security import hash_password

def create_admin():
    db = SessionLocal()
    try:
        username = "admin"
        password = "123456"

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
