from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import user_model, reserve_model
from app.schemas import user_schema
from app.utils.auth import hash_password, verify_password, create_access_token

# ユーザー登録
def create_user(
        user: user_schema.UserCreate,
        db: Session
        ) -> user_schema.UserCreateResponse:
    
    db_user = user_model.User(
        name = user.name,
        email = user.email,
        phone_number = user.phone_number,
        hashed_password = hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# ユーザー一覧
def get_users(db: Session) -> list[user_schema.UserCreateResponse]:
    return db.query(user_model.User).all()

# ログイン
def login(form_data: OAuth2PasswordRequestForm, db: Session) -> dict[str, str]:
    user = db.query(user_model.User).filter(user_model.User.id == form_data.id).first()

    if not user:
        raise HTTPException(status_code=400, detail="ユーザーが見つかりませんでした")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="パスワードが違います")

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ユーザー削除
def delete_user(id: str, db: Session):
    db_user = db.query(user_model.User).filter(user_model.User.id == id).one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="該当するユーザーが見つかりませんでした")
    
    db_reservations = db.query(reserve_model.Reservation).filter(
        reserve_model.Reservation.user_id == id
    ).all()

    for db_reservation in db_reservations:
        db.delete(db_reservation)
    db.delete(db_user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)