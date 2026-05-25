from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
from uuid import uuid4
from datetime import datetime
from app.db import Base

# 予約情報
class Reservation(Base):
    __tablename__ = 'reservations'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))

    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)

    pattern_id: Mapped[str] = mapped_column(String)
    people: Mapped[int] = mapped_column(Integer)
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[str | None] = mapped_column(String, ForeignKey('users.id'), nullable=True)

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
    