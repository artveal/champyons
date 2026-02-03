from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from typing import Optional

class GeographyMixin:
    """Add geonames_id to a model"""
    geonames_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True, unique=True, index=True
    )