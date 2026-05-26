from datetime import datetime, time, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.reserve_model import Reservation
from app.models.seat_model import SeatPattern, PatternMember

# patternsの中から、その時間帯に使える席パターンを返す
def get_available_patterns(
        patterns: list[SeatPattern],
        start_at: datetime,
        end_at: datetime,
        db: Session
):
    available_patterns = []

    # 使用可能な席パターンを１つずつ判定
    for pattern in patterns:
        # その席パターンで使われている席（単体）を全て取得
        stmt1 = select(PatternMember.seat_id).where(
                PatternMember.pattern_id == pattern.id
            )
        seat_ids = db.execute(stmt1).scalars().all()

        # その席が同じ時間帯で他の予約で使われていないか判定
        stmt2 = (
            select(PatternMember)
            .join(
                Reservation,
                Reservation.pattern_id == PatternMember.pattern_id
            )
            .where(
                PatternMember.seat_id.in_(seat_ids),

                Reservation.start_at < end_at,
                Reservation.end_at > start_at
            )
        )
        conflict = db.execute(stmt2).first()

        # 衝突してなければその席は使える
        if conflict is None:
            available_patterns.append(pattern)

    return available_patterns