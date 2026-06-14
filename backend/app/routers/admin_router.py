import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_db
from app.models import admin_model
from app.schemas import admin_schema
from app.cruds import admin_crud
from app.utils.auth import get_current_admin

# .envを読み込む
load_dotenv()

router = APIRouter()

# ユーザー登録
@router.post('/admin/register', response_model = admin_schema.AdminCreateResponse)
def create_admin(
    db: Session = Depends(get_db),
    #current_admin: admin_model.Admin = Depends(get_current_admin)
    ):
    admin = admin_schema.AdminCreate(
        name = os.getenv("ADMIN_NAME"),
        password = os.getenv("PASSWORD")
    )
    return admin_crud.create_admin(admin, db)

# ユーザー一覧
@router.get('/admin/admins', response_model = list[admin_schema.AdminCreateResponse])
def get_admins(
    db: Session = Depends(get_db),
    current_admin: admin_model.Admin = Depends(get_current_admin)
    ):
    return admin_crud.get_admins(db)

# ログイン
@router.post('/admin/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return admin_crud.login(form_data, db)

# ユーザー削除
@router.delete('/admin/delete')
def delete_admin(
    current_admin: admin_model.Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    admin_id = current_admin.id
    return admin_crud.delete_admin(admin_id, db)

# 休業日作成
@router.post('/closed_date', response_model = admin_schema.ClosedDateCreateResponse)
def create_closed_date(
    closed_date: admin_schema.ClosedDateCreate,
    db: Session = Depends(get_db),
    current_admin: admin_model.Admin = Depends(get_current_admin)
):
    return admin_crud.create_closed_date(closed_date, db)

# 休業日一覧取得
@router.get('/closed_dates', response_model = list[admin_schema.ClosedDateCreateResponse])
def get_closed_dates(db: Session = Depends(get_db)):
    return admin_crud.get_closed_dates(db)

# 休業日削除
@router.delete('/closed_date/{closed_id}')
def delete_closed_date(
    closed_id: int,
    db: Session = Depends(get_db),
    current_admin: admin_model.Admin = Depends(get_current_admin)
):
    return admin_crud.delete_closed_date(closed_id, db)