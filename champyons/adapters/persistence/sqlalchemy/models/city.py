import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship      

from ..base import Base
from ..mixins import GeographyMixin, TimestampMixin, ActiveMixin
from .translation import Translation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation
    from .local_region import LocalRegion

class City(Base, ActiveMixin, GeographyMixin, TimestampMixin):
    __tablename__ = "city"

    # Columns
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    default_name: Mapped[str] = mapped_column(sa.String, index=True, info={"translatable": True})
    population_range: Mapped[int] = mapped_column(sa.SmallInteger, default=0)
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    altitude: Mapped[int] = mapped_column(nullable=True) 

    # Foreign Keys
    nation_id: Mapped[int] = mapped_column(sa.ForeignKey("nation.id"), index=True)
    local_region_id: Mapped[int] = mapped_column(sa.ForeignKey("local_region.id"))

    # Relationships
    nation: Mapped["Nation"] = relationship("Nation", back_populates="cities", lazy="joined")
    local_region: Mapped["LocalRegion"] = relationship("LocalRegion", back_populates="cities", lazy="joined")


    

