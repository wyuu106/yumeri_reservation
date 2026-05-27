from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, ForeignKey
from app.db import Base

'''
マスタデータ（固定値）
'''

# 席
class Seat(Base):
    __tablename__ = 'seats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

# 使用できる席（組み合わせを含む）
class SeatPattern(Base):
    __tablename__ = 'seat_patterns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    seat_type: Mapped[str] = mapped_column(String)
    is_private: Mapped[bool] = mapped_column(Boolean)
    min_people: Mapped[int] = mapped_column(Integer)
    max_people: Mapped[int] = mapped_column(Integer)

# パターンに使われている席
class PatternMember(Base):
    __tablename__ = 'pattern_members'

    pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('seat_patterns.id'),
        primary_key=True
        )
    
    seat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('seats.id'),
        primary_key=True
        )