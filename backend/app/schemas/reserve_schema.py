from pydantic import BaseModel
from datetime import datetime

class ReservationCreate(BaseModel):
    people: int
    start_at: datetime

class ReservationCreateResponse(BaseModel):
    start_at: datetime
    end_at: datetime