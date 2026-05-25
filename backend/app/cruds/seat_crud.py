from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from datetime import datetime
from app.models import reserve_model, seat_model

def get_reserved_seats(
        start_at: datetime,
        end_at: datetime,
        db: Session
        ) -> list[seat_model.Seat]:
    
    1

    
