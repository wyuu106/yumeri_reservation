from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from typing import Optional
from uuid import uuid4
from datetime import datetime
from app.db import Base

# 予約情報
class Reservation(Base):
    __tablename__ = 'reservations'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))

    name: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    pattern_id: Mapped[str] = mapped_column(String, ForeignKey('seat_patterns.id'))

    people: Mapped[int] = mapped_column(Integer)
    kids: Mapped[int] = mapped_column(Integer)
    start_at: Mapped[datetime] = mapped_column(DateTime, timezone=True)
    end_at: Mapped[datetime] = mapped_column(DateTime, timezone=True)

# 予約に使用されている席の情報
class ReservedSeat(Base):
    __tablename__ = 'reserved_seats'

    reservation_id: Mapped[str] = mapped_column(
        String,
        ForeignKey('reservations.id'),
        primary_key=True
        )
    
    seat_id: Mapped[str] = mapped_column(
        String,
        ForeignKey('seats.id'),
        primary_key=True
        )
    