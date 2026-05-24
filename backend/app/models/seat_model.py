from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from app.db import Base

# 席
class Seat(Base):
    __tablename__ = 'seats'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)

# 使用できる席（組み合わせを含む）
class SeatPattern(Base):
    __tablename__ = 'seat_patterns'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    capacity: Mapped[int] = mapped_column(Integer)

# 席のパターンに使われている席
class PatternMember(Base):
    __tablename__ = 'pattern_members'

    pattern_id: Mapped[str] = mapped_column(
        String,
        ForeignKey('SeatPattern.id'),
        primary_key=True
        )
    
    seat_id: Mapped[str] = mapped_column(
        String,
        ForeignKey('Seat.id'),
        primary_key=True
        )