from sqlalchemy import Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from champyons.core.domain.entities.geography.region import Region as RegionEntity, RegionTypeEnum

from ..base import Base
from ..mixins import ActiveMixin, GeographyMixin, TimestampMixin

from .translation import Translation
from .country_region import country_region_table

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .country import Country

class Region(Base, ActiveMixin, GeographyMixin, TimestampMixin):
    __tablename__ = "region"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    default_name: Mapped[str] = mapped_column(String, index=True, info={"translatable": True})
    type: Mapped[int] = mapped_column(SmallInteger, default=1)

    # Relationships
    countries: Mapped[list["Country"]] = relationship(
        "Country",
        secondary=country_region_table,
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

    def to_entity(self, *, include_countries = False) -> RegionEntity:
        return RegionEntity(
            id=self.id,
            type=RegionTypeEnum(self.type),
            name=self.default_name,
            geonames_id=self.geonames_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
            countries=[country.to_entity() for country in self.countries] if include_countries else []
        )
    
    

