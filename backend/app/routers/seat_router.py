from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from fastapi import Response, HTTPException, status
from app.db import get_db
from app.utils.auth import get_current_admin
from app.models.admin_model import Admin
from app.models.seat_model import Seat, SeatPattern, PatternMember
from app.schemas.seat_schema import SeatCreate, SeatPatternCreate, PatternMemberCreate

router = APIRouter()

# 席作成
@router.post('/admin/seats', response_model = SeatCreate)
def create_seat(
    seat_data: SeatCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    db_seat = Seat(id = seat_data.id, name = seat_data.name)

    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)

    return db_seat

# 席パターン作成
@router.post('/admin/patterns', response_model = SeatPatternCreate)
def create_seat(
    pattern_data: SeatPatternCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    db_pattern = SeatPattern(
        id = pattern_data.id,
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
@router.post('/admin/members', response_model = PatternMemberCreate)
def create_seat(
    member_data: PatternMemberCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    db_member = PatternMember(
        pattern_id = member_data.pattern_id,
        seat_id = member_data.seat_id
        )
    
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member

# 席情報取得
@router.get('/admin/seats', response_model = list[SeatCreate])
def get_seats(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    return db.execute(select(Seat)).scalars().all()

# 席パターン取得
@router.get('/admin/patterns', response_model = list[SeatPatternCreate])
def get_seats(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    return db.execute(select(SeatPattern)).scalars().all()

# 席パターンに使われている席情報取得
@router.get('/admin/members', response_model = list[PatternMemberCreate])
def get_seats(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    return db.execute(select(PatternMember)).scalars().all()

# 席削除
@router.delete('/admin/seat')
def delete_saet(
    seat_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    db_seat = db.execute(select(Seat).where(Seat.id == seat_id)).scalar_one_or_none()

    if not db_seat:
        raise HTTPException(status_code=404, detail="該当する席が見つかりませんでした")
    
    # 紐付け解除
    db.execute(delete(PatternMember).where(PatternMember.seat_id == seat_id))

    db.delete(db_seat)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 席パターン削除
@router.delete('/admin/pattern')
def delete_pattern(
    pattern_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    db_pattern = db.execute(
        select(SeatPattern).where(SeatPattern.id == pattern_id)
        ).scalar_one_or_none()

    if not db_pattern:
        raise HTTPException(status_code=404, detail="該当する席パターンが見つかりませんでした")
    
    # 紐付け解除
    db.execute(delete(PatternMember).where(PatternMember.pattern_id == pattern_id))

    db.delete(db_pattern)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)