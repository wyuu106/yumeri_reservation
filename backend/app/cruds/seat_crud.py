from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from fastapi import Response, HTTPException, status
from app.db import get_db
from app.utils.auth import get_current_admin
from app.models import admin_model
from app.models import seat_model
from app.schemas import seat_schema

# 席情報作成
def create_seat(
        seat_data: seat_schema.SeatCreate,
        db: Session
) -> seat_schema.SeatCreateResponse:
    db_seat = seat_model.Seat(name = seat_data.name)

    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)

    return db_seat

# 席パターン作成
def create_pattern(
        pattern_data: seat_schema.SeatPatternCreate,
        db: Session
) -> seat_schema.SeatPatternCreateResponse:
    db_pattern = seat_model.SeatPattern(
        name = pattern_data.name,
        seat_type = pattern_data.seat_type,
        is_private = pattern_data.is_private,
        min_people = pattern_data.min_people,
        max_people = pattern_data.max_people
    )

    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)

    return db_pattern

# 席パターンに使われている席作成
def create_member(
        member_data: seat_schema.PatternMemberCreate,
        db: Session
) -> seat_schema.PatternMemberCreate:
    db_member = seat_model.PatternMember(
        pattern_id = member_data.pattern_id,
        seat_id = member_data.seat_id
        )
    
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member

# 席一覧
def get_seats(db: Session) -> list[seat_schema.SeatCreateResponse]:
    return db.execute(select(seat_model.Seat)).scalars().all()

# 席パターン一覧
def get_patterns(db: Session) -> list[seat_schema.SeatPatternCreateResponse]:
    return db.execute(select(seat_model.SeatPattern)).scalars().all()

# 席パターンに使われている席取得
def get_members(pattern_id: int, db: Session) -> list[seat_schema.SeatCreateResponse]:
    stmt = select(seat_model.Seat).join(
        seat_model.SeatPattern,
        seat_model.Seat.id == seat_model.SeatPattern.seat_id
    ).where(
        seat_model.PatternMember.pattern_id == pattern_id
    )

    return db.execute(stmt).scalars().all()

# 席情報削除
def delete_seat(seat_id: int, db: Session):
    db_seat = db.execute(select(seat_model.Seat).where(
        seat_model.Seat.id == seat_id
    )).scalar_one_or_none()

    if not db_seat:
        raise HTTPException(status_code=404, detail="該当する席が見つかりませんでした")
    
    # 紐付け解除
    db.execute(delete(seat_model.PatternMember).where(
        seat_model.PatternMember.seat_id == seat_id
    ))

    db.delete(db_seat)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 席パターン削除
def delete_pattern(pattern_id: int, db: Session):
    db_pattern = db.execute(select(seat_model.SeatPattern).where(
        seat_model.SeatPattern.id == pattern_id
    )).scalar_one_or_none()

    if not db_pattern:
        raise HTTPException(status_code=404, detail="該当する席パターンが見つかりませんでした")
    
    # 紐付け解除
    db.execute(delete(seat_model.PatternMember).where(
        seat_model.PatternMember.pattern_id == pattern_id
    ))

    db.delete(db_pattern)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)