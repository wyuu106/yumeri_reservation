from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.db import get_db
from app.schemas import reserve_schema
from app.cruds import reserve_crud
from app.utils.auth import get_current_admin
from app.models import admin_model

router = APIRouter()

# 人数、時間、席の条件　から　予約可能な時間帯を返す
@router.get('/availability', response_model=list[reserve_schema.AvailabilityQueryResponse])
def get_availability(
    reservation_date: date,
    people: int,
    kids: int,
    seat_type: str,
    course: str,
    is_private: bool,
    db: Session = Depends(get_db)
    ):
    data = reserve_schema.AvailabilityQuery(
        reservation_date = reservation_date,
        people = people,
        kids = kids,
        seat_type = seat_type,
        course = course,
        is_private = is_private
    )
    return reserve_crud.get_availability(data, db)

# 予約作成（ユーザー）
@router.post('/reservations', response_model = reserve_schema.ReservationCreateResponse)
def create_reservation(
    data: reserve_schema.ReservationCreate,
    db: Session = Depends(get_db)
    ):
    return reserve_crud.create_reservation(data, db)

# 予約作成（管理者用）
@router.post('/admin/reservations', response_model = reserve_schema.ReservationData)
def create_admin_reservation(
    data: reserve_schema.ReservationCreate,
    end_at: datetime,
    db: Session = Depends(get_db),
    current_admin: admin_model.Admin = Depends(get_current_admin) #管理者認証
    ):
    return reserve_crud.create_admin_reservation(data, end_at, db)

# 予約更新
@router.put('/admin/reservations/{reservation_id}', response_model = reserve_schema.ReservationData)
def update_reservation(
    reservation_id: str,
    new_data: reserve_schema.ReservationUpdate,
    db: Session = Depends(get_db),
    current_admin: admin_model.Admin = Depends(get_current_admin) # 管理者認証
):
    return reserve_crud.update_reservation(reservation_id, new_data, db)

# 予約キャンセル
@router.delete('/reservations/{reservation_id}')
def delete_reservation(
    reservation_id: str,
    phone_number: str,
    db: Session = Depends(get_db)
    ):
    return reserve_crud.delete_reservation(reservation_id, phone_number, db)

# その日の予約取得（管理者用）
@router.get('/admin/reservations/day', response_model = list[reserve_schema.ReservationData])
def get_reservations(
    date: date,
    db: Session = Depends(get_db),
    current_admin: admin_model.Admin = Depends(get_current_admin) # 管理者認証
    ):
    return reserve_crud.get_reservations(date, db)

# 全予約取得（開発者用）
@router.get('/all_reservations', response_model = list[reserve_schema.ReservationData])
def get_all_reservations(
    db: Session = Depends(get_db),
    current_admin: admin_model.Admin = Depends(get_current_admin) # 管理者認証
    ):
    return reserve_crud.get_all_reservations(db)