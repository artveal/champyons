from sqlalchemy import  Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from ..mixins import GeographyMixin, TimestampMixin, ActiveMixin

from champyons.core.domain.entities.nation import Nation as NationEntity

from .continent import Continent
from .region import Region
from .local_region import LocalRegion
from .city import City
from .translation import Translation

from typing import Optional, List

class Nation(Base, ActiveMixin, GeographyMixin, TimestampMixin):
    __tablename__ = "nation"
    
    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    default_name: Mapped[str] = mapped_column(String, index=True, nullable=False, info={"translatable": True})
    
    is_world_federation_member: Mapped[bool] = mapped_column(Boolean, default=False)
    is_confederation_member: Mapped[bool] = mapped_column(Boolean, default=False)

    continent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("continent.id"), index=True)
    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("region.id"), index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("nation.id"), index=True, nullable=True, default=None)

    # Relationships
    continent: Mapped[Optional[Continent]] = relationship("Continent", back_populates="nations", lazy="joined")
    region: Mapped[Optional[Region]] = relationship("Region", back_populates="nations", lazy="joined")
    cities: Mapped[List[City]] = relationship("City", back_populates="nation")
    local_regions: Mapped[List[LocalRegion]] = relationship("LocalRegion", back_populates="nation", foreign_keys="LocalRegion.nation_id")

    # Self-referential
    parent: Mapped[Optional["Nation"]] = relationship("Nation", remote_side=[id], back_populates="children")
    children: Mapped[List["Nation"]] = relationship("Nation", back_populates="parent")

    @classmethod
    def from_entity(cls, entity: NationEntity) -> "Nation":
        return cls(
            id = entity.id,
            code = entity.code,
            default_name = entity.name,
            is_world_federation_member = entity.is_world_federation_member,
            is_confederation_member = entity.is_confederation_member,
            continent_id = entity.continent_id,
            region_id = entity.region_id,
            parent_id = entity.parent_id,
            active =  entity.active,
            geonames_id = entity.geonames_id,
        )
    
    def update_from_entity(self, entity: NationEntity) -> None:
        self.code = entity.code
        self.default_name = entity.name
        self.is_world_federation_member = entity.is_world_federation_member
        self.is_confederation_member = entity.is_confederation_member
        self.continent_id = entity.continent_id
        self.region_id = entity.region_id
        self.parent_id = entity.parent_id
        self.active =  entity.active
        self.geonames_id = entity.geonames_id
    
    def to_entity(self, *, include_continent: bool = True, include_region: bool = True, include_parent: bool = True,  include_children: bool = False) -> NationEntity:
        return NationEntity(
            id=self.id,
            code=self.code,
            name=self.default_name,
            is_world_federation_member=self.is_world_federation_member,
            is_confederation_member=self.is_confederation_member,
            continent_id=self.continent_id,
            region_id=self.region_id,
            parent_id=self.parent_id,
            active=self.active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            geonames_id=self.geonames_id,

            continent=self.continent.to_entity() if include_continent and self.continent else None,
            region=self.region.to_entity() if include_region and self.region else None,
            parent=self.parent.to_entity() if include_parent and self.parent else None,
            children=[child.to_entity() for child in self.children] if include_children else [],
        )
