import os
from datetime import datetime, timedelta
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import user_model

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
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

    expire = datetime.utcnow() + timedelta(days=1)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# ログイン中のユーザーを取得
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(user_model.User).filter(
        user_model.User.id == user_id
    ).first()
    
    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user