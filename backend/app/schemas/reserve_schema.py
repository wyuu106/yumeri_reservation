from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# 予約作成の入力データ１
class ReservationCreate1(BaseModel):
    people: int
    kids: int
    seat_type: str
    is_private: bool

class AvailabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    time: str
    available: bool

# 予約作成の入力データ２
class ReservationCreate2(BaseModel):
    # 変数名: 型ヒント（A または B） = デフォルト値
    start_at: datetime
    name: str
    email: EmailStr | None = None
    phone_number: str | None = None

# ユーザー用の予約情報
class ReservationCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    people: int
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