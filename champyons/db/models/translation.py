from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins import TimestampMixin

from typing import Optional

class Translation(Base, TimestampMixin):
    __tablename__ = "translation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity: Mapped[str] = mapped_column(nullable=False, index=True)  
    foreign_key: Mapped[int] = mapped_column(nullable=False, index=True)  
    field: Mapped[str] = mapped_column(nullable=False, index=True)  
    language: Mapped[str] = mapped_column(nullable=False, index=True) 
    index: Mapped[Optional[int]] = mapped_column(nullable=True, default=None)  
    translation: Mapped[str] = mapped_column(nullable=False) 

    __table_args__ = (
        UniqueConstraint(
            "entity",
            "foreign_key",
            "field",
            "index",
            "language",
            name="uq_translation"
        ),
    )




