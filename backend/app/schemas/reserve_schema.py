from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime

# 予約作成の入力データ１
class AvailabilityQuery(BaseModel):
    reservation_date: date
    people: int
    kids: int
    seat_type: str
    course: str
    is_private: bool

class AvailabilityQueryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    time: str
    available: bool

# 予約作成の入力データ2
class ReservationCreate(BaseModel):
    # 変数名: 型ヒント（A または B） = デフォルト値
    name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None

    people: int
    kids: int
    seat_type: str
    course: str
    is_private: bool
    start_at: datetime

# ユーザー用の予約情報
class ReservationCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    people: int
    course: str
    start_at: datetime

# 店用の予約情報
class ReservationData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    pattern_name: str
    name: str
    people: int
    start_at: datetime
    end_at: datetime

# 予約変更の入力データ
class ReservationUpdate(BaseModel):
    pattern_id: int
    people: int
    start_at: datetime
    end_at: datetime