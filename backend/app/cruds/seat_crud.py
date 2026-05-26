from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from datetime import datetime, time, timedelta
from app.models import seat_model
from app.schemas import seat_schema
from app.utils.seat_util import get_available_patterns

def get_availability(seat_data: seat_schema.SeatData, date: str, db: Session) -> list[dict]:
    # 時間の条件で使用可能な席パターンを取得
    stmt = select(seat_model.SeatPattern).where(
        seat_model.SeatPattern.min_people <= seat_data.people,
        seat_model.SeatPattern.max_people >= seat_data.people
        )
    if seat_data.type != 'any':
        stmt = stmt.where(seat_model.SeatPattern.type == seat_data.type)
    patterns = db.execute(stmt).scalars().all()

    target_date = datetime.strptime(date, "%Y-%m-%d")
    day_start = datetime.combine(target_date, time(18, 0))
    day_end = datetime.combine(target_date, time(22, 0))

    t = day_start

    results = []

    # 30分ごとに、予約の可否を判定
    while t < day_end:
        start_at = t
        end_at = t + timedelta(hours=2, minutes=30)

        # patternsの中から、その時間帯に使える席パターンを取得
        available_patterns = get_available_patterns(
            patterns = patterns,
            start_at = start_at,
            end_at = end_at,
            db = db
        )
        
        results.append({
            "time": start_at.strftime("%H:%M"),
            "available": len(available_patterns) > 0 # 使える席が１つでもあればTrue
        })

        t += timedelta(minutes=30)

    return results