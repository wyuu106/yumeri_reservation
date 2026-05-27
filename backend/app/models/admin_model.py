from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from uuid import uuid4
from app.db import Base

class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)