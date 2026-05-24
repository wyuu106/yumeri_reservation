from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from app.schemas import reserve_schema

# 予約作成
def create_reservation(
        reservation: reserve_schema.ReservationCreate,
        db: Session
        ) -> reserve_schema.ReservationCreateResponse:
    
    1