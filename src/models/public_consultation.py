from datetime import datetime
from typing import Optional

import sqlalchemy.orm
from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..enums.public_consultation_type import PublicConsultationType
from ..utils import get_current_time
from .model_base import ModelBase


class PublicConsultation(ModelBase):
    __tablename__ = "public_consultation"
    id: Mapped[int] = mapped_column(primary_key=True)
    dates: Mapped[str]
    description: Mapped[str]
    last_fetched_at: Mapped[datetime]
    name: Mapped[str]
    subtype: Mapped[Optional[str]]
    type: Mapped[PublicConsultationType] = mapped_column(
        Enum(
            PublicConsultationType,
            values_callable=lambda public_consultation_types: [
                public_consultation_type.value
                for public_consultation_type in public_consultation_types
            ],
        )
    )
    __table_args__ = (
        UniqueConstraint(
            "dates",
            "description",
            "name",
            "subtype",
            "type",
        ),
    )

    def __init__(self, path: str, description: str, fields: dict[str, str]) -> None:
        _, _, typeString, self.name = path.split("/")
        self.type = PublicConsultationType(typeString)
        self.dates = fields[self.type.dates_field_name]
        self.description = description
        self.fields = fields
        self.last_fetched_at = get_current_time()
        self.path = path
        self.subtype = fields.get("Veids")

    @property
    def is_closed(self) -> bool:
        return self.fields.get("Statuss") == "Noslēdzies"

    def retrieve(self, sql_session: sqlalchemy.orm.Session) -> bool:
        existing_public_consultation = (
            sql_session.query(
                PublicConsultation.id,
                PublicConsultation.created_at,
                PublicConsultation.last_fetched_at,
            )
            .filter_by(
                dates=self.dates,
                description=self.description,
                name=self.name,
                subtype=self.subtype,
                type=self.type,
            )
            .one_or_none()
        )
        if existing_public_consultation is not None:
            self.id = existing_public_consultation.id
            self.created_at = existing_public_consultation.created_at
        return existing_public_consultation is not None
