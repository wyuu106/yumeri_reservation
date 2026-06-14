from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date
from datetime import date
from uuid import uuid4
from app.db import Base

class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

# 休業日情報
class ClosedDate(Base):
    __tablename__ = 'closed_dates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    closed_date: Mapped[date] = mapped_column(Date, unique=True)