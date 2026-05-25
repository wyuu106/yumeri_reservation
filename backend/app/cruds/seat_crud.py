from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from datetime import datetime, time, timedelta
from app.models import seat_model, reserve_model
from app.cruds import reserve_crud

def get_availability(people: int, date: str, db: Session):
    # 時間の条件で使用可能な席パターンを取得
    stmt1 = select(seat_model.SeatPattern).where(
        seat_model.SeatPattern.min_people <= people,
        seat_model.SeatPattern.max_people >= people
    )
    patterns = db.execute(stmt1).scalars().all()

    target_date = datetime.strptime(date, "%Y-%m-%d")
    day_start = datetime.combine(target_date, time(18, 0))
    day_end = datetime.combine(target_date, time(22, 0))

    t = day_start

    results = []

    # 30分ごとに、予約の可否を判定
    while t < day_end:
        start_at = t
        end_at = t + timedelta(hours=2, minutes=30)

        available = False

        # 使用可能な席パターンを１つずつ判定
        for pattern in patterns:
            # その席パターンで使われている席（単体）を取得
            stmt2 = select(seat_model.PatternMember.seat_id).where(
                    seat_model.PatternMember.pattern_id == pattern.id
                )
            seat_ids = db.execute(stmt2).scalars().all()

            # その時間帯の席で他の予約で使われているかの判定
            stmt3 = (
                select(seat_model.PatternMember)
                .join(
                    reserve_model.Reservation,
                    reserve_model.Reservation.pattern_id == seat_model.PatternMember.pattern_id
                )
                .where(
                    seat_model.PatternMember.seat_id.in_(seat_ids),

                    reserve_model.Reservation.start_at < end_at,
                    reserve_model.Reservation.end_at > start_at
                )
            )
            conflict = db.execute(stmt3).first()

            # 衝突してなければ使える
            if conflict is None:
                available = True
                break

            results.append({
            "time": start_at.strftime("%H:%M"),
            "available": available
        })

        t += timedelta(minutes=30)

    return results