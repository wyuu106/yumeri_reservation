from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
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