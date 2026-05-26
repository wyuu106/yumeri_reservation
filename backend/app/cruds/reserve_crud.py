from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from datetime import datetime, time, timedelta
from app.models import user_model, reserve_model
from app.schemas import reserve_schema

# 予約作成
def create_reservation(
        data: reserve_schema.ReservationCreate,
        current_user: user_model.User,
        db: Session
        ) -> reserve_schema.ReservationCreateResponse:
    
    # ゲストユーザーの処理
    if current_user is None:
        if data.name is None:
            raise HTTPException(
                status_code=400,
                detail="予約名が未入力です"
            )

        if data.email is None:
            raise HTTPException(
                status_code=400,
                detail="メールアドレスが未入力です"
            )

        if data.phone_number is None:
            raise HTTPException(
                status_code=400,
                detail="電話番号が未入力です"
            )
        
        # それぞれのデータを入力フォームから取得
        name = data.name
        email = data.email
        phone_number = data.phone_number
        user_id = None

    # ログインユーザーの処理
    else:
        # それぞれのデータをユーザー情報から取得
        name = current_user.name
        email = current_user.email
        phone_number = current_user.phone_number
        user_id = current_user.id

    db_reservation = reserve_model.Reservation(
        name = name,
        email = email,
        phone_number = phone_number,
        people = data.people,
        kid = data.kid,
        start_at = data.start_at,
        end_at = data.start_at + timedelta(hours=2, minites=30),
        user_id = user_id
    )

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約キャンセル
def delete_reservation(
        reservation_id: str,
        db: Session
):
    
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.id == reservation_id
    )
    db_reservation = db.execute(stmt).scalar_one_or_none()

    if not db_reservation:
        raise HTTPException(status_code=404, detail="該当する予約が見つかりませんでした")

    db.delete(db_reservation)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ユーザーごとの予約取得
def get_user_reservations(
        user_id: str, db: Session
        ) -> list[reserve_schema.ReservationCreateResponse]:
    
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.user_id == user_id
    )
    db_reservations = db.execute(stmt).scalars().all()

    return db_reservations

# 特定日の予約を全て取得（管理者用）
def get_reservations(date: str, db: Session) -> list[reserve_schema.ReservationData]:
    target_date = datetime.strptime(date, "%Y-%m-%d")

    day_start = datetime.combine(target_date, time(18, 0))
    day_end = datetime.combine(target_date, time(22, 0))

    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.start_at <= day_end,
        reserve_model.Reservation.end_at >= day_start
    )
    reservations = db.execute(stmt).scalars().all()

    return reservations

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