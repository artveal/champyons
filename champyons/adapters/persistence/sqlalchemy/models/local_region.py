from sqlalchemy import  Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from ..mixins import ActiveMixin, GeographyMixin, TimestampMixin

from .city import City
from .translation import Translation

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .country import Country
    
class LocalRegion(Base, ActiveMixin, GeographyMixin, TimestampMixin):
    __tablename__ = "local_region"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    default_name: Mapped[str] = mapped_column(String, index=True, nullable=False, info={"translatable": True})

    # Foreign Keys
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"), index=True, nullable=False)
    parent_local_region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("local_region.id"), index=True, nullable=True)
    other_countryality_id: Mapped[Optional[int]] = mapped_column(ForeignKey("country.id"), nullable=True)

    # Relationships
    country: Mapped["Country"] = relationship(back_populates="local_regions", lazy="joined", foreign_keys=[country_id])
    cities: Mapped[list["City"]] = relationship(back_populates="local_region", lazy="joined")
    other_countryality: Mapped["Country"] = relationship(foreign_keys=[other_countryality_id])

    # Self-referential relationships
    parent: Mapped[Optional["LocalRegion"]] = relationship("LocalRegion", remote_side=[id], back_populates="children", lazy="joined")
    children: Mapped[list["LocalRegion"]] = relationship("LocalRegion", back_populates="parent", lazy="joined")

    