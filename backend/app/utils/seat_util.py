from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reserve_model import Reservation
from app.models.seat_model import SeatPattern, PatternMember
from app.schemas.reserve_schema import ReservationCreate1

# 予約条件に合った席パターンを取得
def get_candidate_patterns(
        data: ReservationCreate1,
        db: Session
        ):
    
    stmt = select(SeatPattern).where(
        SeatPattern.min_people <= data.people,
        SeatPattern.max_people >= data.people
        )
    if data.seat_type != 'any':
        stmt = stmt.where(SeatPattern.seat_type == data.seat_type)
    if data.is_private:
        stmt = stmt.where(SeatPattern.is_private == True)
    
    patterns = db.execute(stmt).scalars().all()

    return patterns

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

def assign_pattern(
        data: ReservationCreate1,
        start_at: datetime,
        end_at: datetime,
        db: Session
        ):
    
    patterns = get_candidate_patterns(data, db)

    available_patterns = get_available_patterns(patterns, start_at, end_at, db)

    if not available_patterns:
        raise HTTPException(status_code=400, detail="予約可能な席がありません")

    return available_patterns[0].id