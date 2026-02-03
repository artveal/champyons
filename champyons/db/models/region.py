from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from champyons.core.domain.entities.region import Region as RegionEntity

from ..base import Base
from ..mixins import ActiveMixin, GeographyMixin, TimestampMixin

from .translation import Translation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation

class Region(Base, ActiveMixin, GeographyMixin, TimestampMixin):
    __tablename__ = "region"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    default_name: Mapped[str] = mapped_column(String, index=True, info={"translatable": True})

    # Relationships
    nations: Mapped[list["Nation"]] = relationship("Nation", back_populates="region")

    @classmethod
    def from_entity(cls, entity: RegionEntity) -> "Region":
        return cls(
            id=entity.id,
            default_name=entity.name,
            geonames_id=entity.geonames_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            active=entity.active,
        ) 
    
    def update_from_entity(self, entity: RegionEntity):
        self.default_name = entity.name
        self.geonames_id = entity.geonames_id
        self.active = entity.active

    def to_entity(self, *, include_nations = False) -> RegionEntity:
        return RegionEntity(
            id=self.id,
            name=self.default_name,
            geonames_id=self.geonames_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
            nations=[nation.to_entity() for nation in self.nations] if include_nations else []
        )
    
    

