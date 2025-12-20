from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.admin import Admin
from app.utils.security import verify_password, create_access_token
from app.models import AdminUser

router = APIRouter(prefix="/admin", tags=["Admin Auth"])

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    admin = db.query(AdminUser).filter(AdminUser.username == username).first()

    if not admin or not verify_password(password, str(admin.password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": admin.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
