from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from fastapi import Response, HTTPException, status
from app.db import get_db
from app.utils.auth import get_current_admin
from app.models.admin_model import Admin
from app.schemas import seat_schema
from app.cruds import seat_crud

router = APIRouter()

# 席作成
@router.post('/admin/seats', response_model=seat_schema.SeatCreateResponse)
def create_seat(
    seat_data: seat_schema.SeatCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    return seat_crud.create_seat(seat_data, db)

# 席パターン作成
@router.post('/admin/patterns', response_model=seat_schema.SeatPatternCreateResponse)
def create_pattern(
    pattern_data: seat_schema.SeatPatternCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    return seat_crud.create_pattern(pattern_data, db)

# 席パターンに使われている席作成
@router.post('/admin/members', response_model=seat_schema.PatternMemberCreate)
def create_member(
    member_data: seat_schema.PatternMemberCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    return seat_crud.create_member(member_data, db)

# 席情報取得
@router.get('/admin/seats', response_model=list[seat_schema.SeatCreateResponse])
def get_seats(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    return seat_crud.get_seats(db)

# 席パターン取得
@router.get('/admin/patterns', response_model=list[seat_schema.SeatPatternCreateResponse])
def get_patterns(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    return seat_crud.get_patterns(db)

# 席パターンに使われている席情報取得
@router.get('/admin/members', response_model = list[seat_schema.SeatCreateResponse])
def get_members(
    pattern_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    return seat_crud.get_members(pattern_id, db)

# 席削除
@router.delete('/admin/seat')
def delete_saet(
    seat_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    return seat_crud.delete_seat(seat_id, db)

# 席パターン削除
@router.delete('/admin/pattern')
def delete_pattern(
    pattern_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
    ):
    return seat_crud.delete_pattern(pattern_id, db)