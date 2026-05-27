import os
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import admin_model

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# パスワードのハッシュ化
def hash_password(password: str):
    return pwd_context.hash(password)

# パスワード確認
def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=1)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login"
)

# 管理者認証用
def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        admin_id = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="認証に失敗しました"
        )

    admin = db.execute(select(admin_model.Admin).where(
        admin_model.Admin.id == admin_id
    )).scalar_one_or_none()

    if admin is None:
        raise HTTPException(
            status_code=401,
            detail="認証に失敗しました"
        )

    return admin