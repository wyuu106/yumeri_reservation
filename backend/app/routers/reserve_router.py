from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import get_db
from app.models import user_model, reserve_model
from app.schemas import reserve_schema
from app.cruds import reserve_crud
from app.utils.auth import get_optional_user

router = APIRouter()

# 予約作成
@router.post('/reservations', response_model = reserve_schema.ReservationCreateResponse)
def create_reservation(
    data: reserve_schema.ReservationCreate,
    current_user: user_model.User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    return reserve_crud.create_reservation(data, current_user, db)

# 予約キャンセル
@router.delete('/reservations/{reservation_id}')
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    return reserve_crud.delete_reservation(reservation_id, db)

# ユーザーごとの予約一覧取得（ユーザー用）
@router.get('/reservations/', response_model = list[reserve_schema.ReservationCreateResponse])
def get_user_reservations(
    current_user: user_model.User = Depends(get_optional_user),
    db: Session = Depends(get_db)
    ):
    user_id = current_user.id
    return reserve_crud.get_user_reservations(user_id, db)

# その日の予約取得（管理者用）
@router.get('/day_reservations', response_model = list[reserve_schema.ReservationData])
def get_reservations(date: datetime, db: Session = Depends(get_db)):
    return reserve_crud.getreservations(date, db)

# 全予約取得（開発者用）
@router.get('all_reservations', response_model = reserve_model.Reservation)
def get_all_reservations(db: Session = Depends(get_db)):
    return reserve_crud.get_all_reservations(db)