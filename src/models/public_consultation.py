import json
from datetime import datetime
from hashlib import sha256
from typing import Optional

import sqlalchemy.orm
from sqlalchemy import Enum, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import LargeBinary

from ..enums.public_consultation_type import PublicConsultationType
from .model_base import ModelBase


class PublicConsultation(ModelBase):
    __tablename__ = "public_consultation"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[PublicConsultationType] = mapped_column(
        Enum(
            PublicConsultationType,
            values_callable=lambda public_consultation_types: [
                public_consultation_type.value
                for public_consultation_type in public_consultation_types
            ],
        )
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    subtype: Mapped[Optional[str]] = mapped_column(String(255))
    dates: Mapped[str] = mapped_column(String(255))
    hash: Mapped[bytes] = mapped_column(LargeBinary(32))
    last_fetched_at: Mapped[datetime]
    __table_args__ = (Index("idx_hash", "hash", unique=True, mysql_length=32),)

    def __init__(
        self,
        path: str,
        description: str,
        fields: dict[str, str],
        public_consultation_type: PublicConsultationType,
    ) -> None:
        _, _, self.name = path.split("/", 2)
        self.type = public_consultation_type
        self.dates = fields[self.type.dates_field_name]
        self.description = description
        self.fields = fields
        self.last_fetched_at = datetime.now()
        self.path = path
        self.subtype = fields.get("Veids")
        string_to_hash = json.dumps(
            [self.type.value, self.name, self.description, self.subtype, self.dates],
            separators=(",", ":"),
            ensure_ascii=False,
        )
        self.hash = sha256(string_to_hash.encode()).digest()

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
