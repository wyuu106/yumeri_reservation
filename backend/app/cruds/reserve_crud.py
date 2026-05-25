from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from datetime import timedelta
from app.models import user_model, reserve_model
from app.schemas import reserve_schema

# 予約作成
def create_reservation(
        current_user: user_model.User,
        data: reserve_schema.ReservationCreate,
        db: Session
        ) -> reserve_schema.ReservationCreateResponse:
    
    # ゲストユーザーの処理
    if current_user in None:
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
        name = data.nema
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