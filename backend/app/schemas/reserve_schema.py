from pydantic import BaseModel, EmailStr
from datetime import datetime

class ReservationCreate(BaseModel):
    # 変数名: 型ヒント（A または B） = デフォルト値
    name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None

    people: int
    start_at: datetime

class ReservationCreateResponse(BaseModel):
    id: str
    name: str
    people: int
    start_at: datetime
    end_at: datetime

class ReservationUpdate(BaseModel):
    reservation_id: str
    people: int
    start_at: datetime