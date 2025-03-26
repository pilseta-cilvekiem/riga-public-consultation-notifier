from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ..utils import get_current_time


class ModelBase(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime(), default=get_current_time())
