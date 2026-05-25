from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_db
from app.models import user_model
from app.schemas import user_schema
from app.cruds import user_crud
from app.utils.auth import get_optional_user

router = APIRouter()

# ユーザー登録
@router.post('/register', response_model = user_schema.UserCreateResponse)
def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
    ):
    return user_crud.create_user(user, db)

# ユーザー一覧
@router.get('/users', response_model = list[user_schema.UserCreateResponse])
def get_users(db: Session = Depends(get_db)):
    return user_crud.get_users(db)

# ログイン
@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user_crud.login(form_data, db)

# ユーザー削除
@router.delete('/users/me')
def delete_user(
    current_user: user_model.User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    return user_crud.delete_user(user_id, db)