from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_db
from app.models import user_model
from app.schemas import reserve_schema
from app.cruds import reserve_crud
from app.utils.auth import get_optional_user

router = APIRouter()

@router.post('/reservation', response_model = reserve_schema.ReservationCreateResponse)
def create_reservation(
    data: reserve_schema.ReservationCreate,
    current_user: user_model.User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    return reserve_crud.create_reservation(data, current_user, db)