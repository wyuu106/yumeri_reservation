from pydantic import BaseModel, EmailStr
from datetime import datetime

# 予約作成の入力データ１
class ReservationCreate1(BaseModel):
    people: int
    type: str
    is_private: bool

# 予約作成の入力データ２
class ReservationCreate2(BaseModel):
    # 変数名: 型ヒント（A または B） = デフォルト値
    start_at: datetime
    name: str
    email: EmailStr | None = None
    phone_number: str | None = None

# ユーザー用の予約情報
class ReservationCreateResponse(BaseModel):
    id: str
    name: str
    people: int
    start_at: datetime

# 店用の予約情報
class ReservationData(BaseModel):
    id: str
    pattern_id: str
    name: str
    people: int
    start_at: datetime
    end_at: datetime

# 予約変更の入力データ
class ReservationUpdate(BaseModel):
    pattern_id: str
    people: int
    start_at: datetime
    end_at: datetime