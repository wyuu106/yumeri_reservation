from pydantic import BaseModel, EmailStr
from datetime import datetime

# 予約作成の入力データ
class ReservationCreate(BaseModel):
    # 変数名: 型ヒント（A または B）
    name: str
    email: EmailStr | None
    phone_number: str | None
    people: int
    start_at: datetime

# ユーザー用の予約情報
class ReservationCreateResponse(BaseModel):
    id: str
    name: str
    people: int
    start_at: datetime
    end_at: datetime

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