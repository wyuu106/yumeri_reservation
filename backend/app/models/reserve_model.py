from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
from uuid import uuid4
from datetime import datetime
from app.db import Base

class Reservation(Base):
    __tablename__ = 'reservations'

    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()))
    people: Mapped[int] = mapped_column(Integer)
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[str] = mapped_column(String, ForeignKey())