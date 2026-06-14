from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from app.models import admin_model
from app.schemas import admin_schema
from app.utils.auth import hash_password, verify_password, create_access_token

# ユーザー登録
def create_admin(
        admin: admin_schema.AdminCreate,
        db: Session
        ) -> admin_schema.AdminCreateResponse:
    
    db_admin = admin_model.Admin(
        name = admin.name,
        hashed_password = hash_password(admin.password)
    )

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return db_admin

# ユーザー一覧
def get_admins(db: Session) -> list[admin_schema.AdminCreateResponse]:
    return db.execute(select(admin_model.Admin)).scalars().all()

# ログイン
def login(form_data: OAuth2PasswordRequestForm, db: Session) -> dict[str, str]:
    stmt = select(admin_model.Admin).where(admin_model.Admin.name == form_data.username)
    admin = db.execute(stmt).scalar_one_or_none()

    if admin is None or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(status_code=400, detail="IDまたはパスワードが違います")

    access_token = create_access_token(
        data={"sub": str(admin.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ユーザー削除
def delete_admin(id: str, db: Session):
    stmt = select(admin_model.Admin).where(admin_model.Admin.id == id)
    db_admin = db.execute(stmt).scalar_one_or_none()

    if not db_admin:
        raise HTTPException(status_code=404, detail="該当するユーザーが見つかりませんでした")
    
    db.delete(db_admin)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 休業日作成
def create_closed_date(
        date: admin_schema.ClosedDateCreate,
        db: Session
) -> admin_schema.ClosedDateCreateResponse:
    
    exist_date = db.execute(select(admin_model.ClosedDate).where(
        admin_model.ClosedDate.closed_date == date
    )).scalar_one_or_none()

    if not exist_date:
        raise HTTPException(status_code=400, detail='既に登録されています')
    
    db_date = admin_model.ClosedDate(closed_date = date)

    db.add(db_date)
    db.commit()
    db.refresh(db_date)

    return db_date

# 休業日一覧
def get_closed_dates(db: Session) -> list[admin_schema.ClosedDateCreateResponse]:
    today = date.today()

    # 来月を取得
    next_month = today + relativedelta(months=1)

    # 来月末の日付を取得
    # calendaer.monthrange(年, 月) = (その月の１日の曜日, その月の最終日)
    end_day = calendar.monthrange(next_month.year, next_month.month)[1]

    # 来月末をdate型にする
    next_month_end = date(next_month.year, next_month.month, end_day)

    stmt = select(admin_model.ClosedDate).where(
        admin_model.ClosedDate.closed_date >= today + timedelta(days=1),
        admin_model.ClosedDate.closed_date <= next_month_end
    )
    db_dates = db.execute(stmt).scalars().all()

    return db_dates

# 休業日削除
def delete_closed_date(closed_id: int, db: Session):
    stmt = select(admin_model.ClosedDate).where(
        admin_model.ClosedDate.id == closed_id
    )
    db_date = db.execute(stmt).scalar_one_or_none()

    if not db_date:
        raise HTTPException(status_code=404, detail='該当する休業日が見つかりませんでした')
    
    db.delete(db_date)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)