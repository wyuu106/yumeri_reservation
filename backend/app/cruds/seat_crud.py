from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from datetime import datetime, time
from app.models import seat_model
from app.cruds import reserve_crud

def get_available_seat(people: int, date: str, db: Session):
    stmt = select(seat_model.SeatPattern).where(
        seat_model.SeatPattern.min_people <= people,
        seat_model.SeatPattern.max_people >= people
    )
    patterns = db.execute(stmt).scalars().all()

    reservations = reserve_crud.get_reservations(date, db)