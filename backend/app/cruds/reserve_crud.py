from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from datetime import timedelta
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
        end_at = data.start_at + timedelta(hours=2),
        user_id = user_id
    )

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 全予約取得
def get_all_reservations(db: Session) -> list[reserve_model.Reservation]:
    all_reservations = db.query(reserve_model.Reservation).all()
    return all_reservations

# ユーザーごとの予約取得
def get_reservations(user_id: str, db: Session) -> list[reserve_schema.ReservationCreateResponse]:
    db_reservations = db.query(reserve_model.Reservation).filter(
        reserve_model.Reservation.user_id == user_id
    ).all()

    return db_reservations

# 予約変更
def update_reservation(
        new_data: reserve_schema.ReservationUpdate,
        db: Session
        ) -> reserve_schema.ReservationCreateResponse:
    
    db_reservation = db.query(reserve_model.Reservation).filter(
        reserve_model.Reservation.id == new_data.reservation_id
    ).first()

    if not db_reservation:
        raise HTTPException(status_code=404, detail="該当する予約が見つかりませんでした")
    
    db_reservation.people = new_data.people
    db_reservation.start_at = new_data.start_at
    db_reservation.end_at = new_data.start_at + timedelta(hours=2)

    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約キャンセル
def delete_reservation(
        reservation_id: str,
        db: Session
):
    
    db_reservation = db.query(reserve_model.Reservation).filter(
        reserve_model.Reservation.id == reservation_id
        ).one_or_none()

    if not db_reservation:
        raise HTTPException(status_code=404, detail="該当する予約が見つかりませんでした")

    db.delete(db_reservation)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
