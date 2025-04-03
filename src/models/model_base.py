from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ModelBase(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now())
