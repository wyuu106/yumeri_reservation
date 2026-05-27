from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_db
from app.models import admin_model
from app.schemas import admin_schema
from app.cruds import admin_crud
from app.utils.auth import get_current_admin

router = APIRouter()

# ユーザー登録
@router.post('/register', response_model = admin_schema.AdminCreateResponse)
def create_admin(
    admin: admin_schema.AdminCreate,
    db: Session = Depends(get_db),
    #current_admin: admin_model.Admin = Depends(get_current_admin)
    ):
    return admin_crud.create_admin(admin, db)

# ユーザー一覧
@router.get('/admins', response_model = list[admin_schema.AdminCreateResponse])
def get_admins(
    db: Session = Depends(get_db),
    #current_admin: admin_model.Admin = Depends(get_current_admin)
    ):
    return admin_crud.get_admins(db)

# ログイン
@router.post('/admin/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return admin_crud.login(form_data, db)

# ユーザー削除
@router.delete('/admins/me')
def delete_admin(
    current_admin: admin_model.Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    admin_id = current_admin.id
    return admin_crud.delete_admin(admin_id, db)