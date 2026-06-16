from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reserve_model import Reservation
from app.models.seat_model import SeatPattern, PatternMember
from app.schemas.reserve_schema import AvailabilityQuery

# 予約条件に合った席パターンを取得
def get_candidate_patterns(
        data: AvailabilityQuery,
        db: Session
) -> list[SeatPattern]:
    
    # 人数から席の候補を取得
    stmt = select(SeatPattern).where(
        SeatPattern.min_people <= data.people,
        SeatPattern.max_people >= data.people
        ).order_by(SeatPattern.max_people)
    # 子供がいる場合
    if data.kids > 0:
        stmt = stmt.where(SeatPattern.seat_type == 'tatami')
    # 席のtypeの指定がある場合
    if data.seat_type != 'any':
        stmt = stmt.where(SeatPattern.seat_type == data.seat_type)
    # 個室希望の場合
    if data.is_private:
        stmt = stmt.where(SeatPattern.is_private == True)
    
    patterns = db.execute(stmt).scalars().all()

    return patterns

# コンフリクト判定
def get_conflict(
        pattern_id: int,
        start_at: datetime,
        end_at: datetime,
        db: Session
):
    # その席パターンで使われている席（単体）を全て取得
    stmt1 = select(PatternMember.seat_id).where(
            PatternMember.pattern_id == pattern_id
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

    return conflict

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
        conflict = get_conflict(pattern.id, start_at, end_at, db)

        # 衝突してなければその席は使える
        if conflict is None:
            available_patterns.append(pattern)

    return available_patterns

# 席の割り当て
def assign_pattern(
        data: AvailabilityQuery,
        start_at: datetime,
        end_at: datetime,
        db: Session
        ):
    
    patterns = get_candidate_patterns(data, db)

    available_patterns = get_available_patterns(patterns, start_at, end_at, db)

    if not available_patterns:
        raise HTTPException(status_code=400, detail="予約可能な席がありません")

    return available_patterns[0]