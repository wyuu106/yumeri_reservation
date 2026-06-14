from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from datetime import date, datetime, time, timedelta
from app.models import reserve_model, seat_model
from app.schemas import reserve_schema
from app.utils.seat_util import get_candidate_patterns, get_available_patterns, assign_pattern

# 人数、時間、席の条件　から　予約可能な時間帯を返す
def get_availability(
        data: reserve_schema.AvailabilityQuery,
        date: date,
        db: Session
        ) -> list[reserve_schema.AvailabilityQueryResponse]:
    
    # 予約条件に合った席パターンを取得
    patterns = get_candidate_patterns(data, db)

    day_start = datetime.combine(date, time(18, 0))
    day_end = datetime.combine(date, time(22, 0))

    if data.people <= 2:
        seat_time = timedelta(hours=2)
    else:
        seat_time = timedelta(hours=2, minutes=30)

    t = day_start

    results = []

    # 15分ごとに、予約の可否を判定
    while t < day_end:
        start_at = t
        end_at = t + seat_time

        # patternsの中から、その時間帯に使える席パターンを取得
        available_patterns = get_available_patterns(
            patterns = patterns,
            start_at = start_at,
            end_at = end_at,
            db = db
        )
        
        results.append(
            reserve_schema.AvailabilityResponse(
                time = start_at.strftime("%H:%M"),
                available = len(available_patterns) > 0 # 使える席が１つでもあればTrue
            )
        )

        t += timedelta(minutes=15)

    return results

# 予約作成（ユーザー）
def create_reservation(
        data: reserve_schema.ReservationCreate,
        db: Session
        ) -> reserve_schema.ReservationCreateResponse:
    
    if data.name is None:
        raise HTTPException(status_code=400, detail="予約名が未入力です")

    if data.email is None:
        raise HTTPException(status_code=400, detail="メールアドレスが未入力です")

    if data.phone_number is None:
        raise HTTPException(status_code=400, detail="電話番号が未入力です")
    
    if data.people <= 2:
        end_at = data.start_at + timedelta(hours=2)
    else:
        end_at = data.start_at + timedelta(hours=2, minutes=30)

    # 選ばれた時間で席を割り当てる
    pattern = assign_pattern(data, data.start_at, end_at, db)

    db_reservation = reserve_model.Reservation(
        name = data.name,
        email = data.email,
        phone_number = data.phone_number,
        pattern_id = pattern.id,
        pattern_name = pattern.name,
        people = data.people,
        kids = data.kids,
        counrse = data.course,
        start_at = data.start_at,
        end_at = end_at
    )

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約作成（管理者用）
def create_admin_reservation(
        pattern_name: str,
        data: reserve_schema.ReservationCreate,
        end_at: datetime,
        db: Session
        ) -> reserve_schema.ReservationData:
    
    if data.name is None:
        raise HTTPException(status_code=400, detail="予約名が未入力です")
    
    stmt = select(seat_model.SeatPattern).where(
        seat_model.SeatPattern.name == pattern_name
    )
    db_pattern = db.execute(stmt).scalar_one_or_none()
    
    db_reservation = reserve_model.Reservation(
        name = data.name,
        email = data.email,
        phone_number = data.phone_number,
        pattern_id = db_pattern.id,
        pattern_name = db_pattern.name,
        people = data.people,
        kids = data.kids,
        course = data.course,
        start_at = data.start_at,
        end_at = end_at
    )

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約変更
def update_reservation(
        reservation_id: str,
        new_data: reserve_schema.ReservationUpdate,
        db: Session
        ) -> reserve_schema.ReservationData:
    
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.id == reservation_id
    )
    db_reservation = db.execute(stmt).scalar_one_or_none()

    db_reservation.pattern_id = new_data.pattern_id
    db_reservation.people = new_data.people
    db_reservation.start_at = new_data.start_at
    db_reservation.end_at = new_data.end_at

    db.commit()
    db.refresh(db_reservation)

    return db_reservation

# 予約キャンセル
def delete_reservation(reservation_id: str, phone_number: str, db: Session):
    
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.id == reservation_id,
        reserve_model.Reservation.phone_number == phone_number
    )
    db_reservation = db.execute(stmt).scalar_one_or_none()

    if not db_reservation:
        raise HTTPException(status_code=404, detail="該当する予約が見つかりませんでした")

    db.delete(db_reservation)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 特定日の予約を全て取得（管理者用）
def get_reservations(date: date, db: Session) -> list[reserve_schema.ReservationData]:
    day_start = datetime.combine(date, time(18, 0))
    day_end = datetime.combine(date, time(22, 0))

    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.start_at <= day_end,
        reserve_model.Reservation.end_at >= day_start
    )
    db_reservations = db.execute(stmt).scalars().all()

    return db_reservations

# 該当するidの予約取得（管理者用）
def get_reservation(reservation_id: str, db: Session) -> reserve_schema.ReservationData:
    stmt = select(reserve_model.Reservation).where(
        reserve_model.Reservation.id == reservation_id
    )
    db_reservation = db.execute(stmt).scalar_one_or_none()

    return db_reservation

# 全予約取得（開発者用）
def get_all_reservations(db: Session) -> list[reserve_schema.ReservationData]:
    all_reservations = db.execute(select(reserve_model.Reservation)).scalars().all()
    return all_reservations