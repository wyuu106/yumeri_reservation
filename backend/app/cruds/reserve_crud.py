from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from datetime import datetime, time, timedelta
from app.models import user_model, reserve_model
from app.schemas import reserve_schema

# 予約作成（ユーザー）
def create_reservation(
        data: reserve_schema.ReservationCreate,
        db: Session
        ) -> reserve_schema.ReservationCreateResponse:
    
    if data.name is None:
        raise HTTPException(status_code=400, detail="予約名が未入力です")

    if data.email is None:
        raise HTTPException(status_code=400, detail="メールアドレスが未入力です")

    if data.phone_number is None:
        raise HTTPException(status_code=400, detail="電話番号が未入力です")
    
    if data.peope <= 2:
        end_at = data.start_at + timedelta(hours=2)
    else:
        end_at = data.start_at + timedelta(hours=2, minutes=30)

    db_reservation = reserve_model.Reservation(
        name = data.name,
        email = data.email,
        phone_number = data.phone_number,
        people = data.people,
        start_at = data.start_at,
        end_at = end_at
    )

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約作成（管理者用）
def create_admin_reservation(
        data: reserve_schema.ReservationCreate,
        end_at: datetime,
        db: Session
        ) -> reserve_schema.ReservationData:
    
    if data.name is None:
        raise HTTPException(status_code=400, detail="予約名が未入力です")
    
    db_reservation = reserve_model.Reservation(
        name = data.name,
        email = data.email,
        phone_number = data.phone_number,
        people = data.people,
        start_at = data.start_at,
        end_at = end_at
    )

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約変更
def update_reservation(
        reservation_id: str,
        new_data: reserve_schema.ReservationUpdate,
        db: Session
        ) -> reserve_schema.ReservationData:
    
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.id == reservation_id
    )
    db_reservation = db.execute(stmt)

    db_reservation.pattern_id = new_data.pattern_id
    db_reservation.people = new_data.people
    db_reservation.start_at = new_data.start_at
    db_reservation.end_at = new_data.end_at

    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約キャンセル
def delete_reservation(reservation_id: str, phone_number: str, db: Session):
    
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.id == reservation_id,
        reserve_model.Reservation.phone_number == phone_number
    )
    db_reservation = db.execute(stmt).scalar_one_or_none()

    if not db_reservation:
        raise HTTPException(status_code=404, detail="該当する予約が見つかりませんでした")

    db.delete(db_reservation)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 特定日の予約を全て取得（管理者用）
def get_reservations(date: str, db: Session) -> list[reserve_schema.ReservationData]:
    target_date = datetime.strptime(date, "%Y-%m-%d")

    day_start = datetime.combine(target_date, time(18, 0))
    day_end = datetime.combine(target_date, time(22, 0))

    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.start_at <= day_end,
        reserve_model.Reservation.end_at >= day_start
    )
    db_reservations = db.execute(stmt).scalars().all()

    return db_reservations

# 該当するidの予約取得（管理者用）
def get_reservation(reservation_id: str, db: Session) -> reserve_model.Reservation:
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.id == reservation_id
    )
    db_reservation = db.execute(stmt).scalar_one_or_none()

    return db_reservation

# 全予約取得（開発者用）
def get_all_reservations(db: Session) -> list[reserve_model.Reservation]:
    all_reservations = db.execute(select(reserve_model.Reservation)).scalars().all()
    return all_reservations