from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from uuid import uuid4
from app.db import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, Primary_Key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)