from sqlalchemy import Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

<<<<<<< HEAD:champyons/adapters/persistence/sqlalchemy/models/region.py
from champyons.core.domain.entities.geography.region import Region as RegionEntity
=======
from champyons.core.domain.entities.region import Region as RegionEntity, RegionTypeEnum
>>>>>>> 35b5f1c71e824f68f09b9635c3f4ab642f80a948:champyons/db/models/region.py

from ..base import Base
from ..mixins import ActiveMixin, GeographyMixin, TimestampMixin

from .translation import Translation
from .nation_region import nation_region_table

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation

class Region(Base, ActiveMixin, GeographyMixin, TimestampMixin):
    __tablename__ = "region"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    default_name: Mapped[str] = mapped_column(String, index=True, info={"translatable": True})
    type: Mapped[int] = mapped_column(SmallInteger, default=1)

    # Relationships
    nations: Mapped[list["Nation"]] = relationship(
        "Nation",
        secondary=nation_region_table,
        back_populates="regions",
        lazy="selectin",
    )


    @classmethod
    def from_entity(cls, entity: RegionEntity) -> "Region":
        return cls(
            id=entity.id,
            type=entity.type.value,
            default_name=entity.name,
            geonames_id=entity.geonames_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            active=entity.active,
        ) 
    
    def update_from_entity(self, entity: RegionEntity):
        self.default_name = entity.name
        self.type = entity.type.value
        self.geonames_id = entity.geonames_id
        self.active = entity.active

    def to_entity(self, *, include_nations = False) -> RegionEntity:
        return RegionEntity(
            id=self.id,
            type=RegionTypeEnum(self.type),
            name=self.default_name,
            geonames_id=self.geonames_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
            nations=[nation.to_entity() for nation in self.nations] if include_nations else []
        )
    
    

