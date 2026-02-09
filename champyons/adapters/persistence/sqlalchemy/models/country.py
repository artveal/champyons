from sqlalchemy import  Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from ..mixins import GeographyMixin, TimestampMixin, ActiveMixin

from champyons.core.domain.entities.geography.country import Country as CountryEntity

from .continent import Continent
from .region import Region
from .local_region import LocalRegion
from .city import City
from .translation import Translation
from .country_region import country_region_table

from typing import Optional, List

class Country(Base, ActiveMixin, GeographyMixin, TimestampMixin):
    __tablename__ = "country"
    
    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    default_name: Mapped[str] = mapped_column(String, index=True, nullable=False, info={"translatable": True})
    
    is_world_federation_member: Mapped[bool] = mapped_column(Boolean, default=False)
    is_confederation_member: Mapped[bool] = mapped_column(Boolean, default=False)

    continent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("continent.id"), index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("country.id"), index=True, nullable=True, default=None)

    # Relationships
    continent: Mapped[Optional[Continent]] = relationship("Continent", back_populates="countrys", lazy="joined")
    regions: Mapped[list["Region"]] = relationship(
        "Region",
        secondary=country_region_table,
        back_populates="countrys",
        lazy="selectin",
    )
    cities: Mapped[List[City]] = relationship("City", back_populates="country")
    local_regions: Mapped[List[LocalRegion]] = relationship("LocalRegion", back_populates="country", foreign_keys="LocalRegion.country_id")

    # Self-referential
    parent: Mapped[Optional["Country"]] = relationship("Country", remote_side=[id], back_populates="children")
    children: Mapped[List["Country"]] = relationship("Country", back_populates="parent")

    @classmethod
    def from_entity(cls, entity: CountryEntity) -> "Country":
        return cls(
            id = entity.id,
            code = entity.code,
            default_name = entity.name,
            continent_id = entity.continent_id,
            parent_id = entity.parent_id,
            active =  entity.active,
            geonames_id = entity.geonames_id,
        )
    
    def update_from_entity(self, entity: CountryEntity) -> None:
        self.code = entity.code
        self.default_name = entity.name
        self.continent_id = entity.continent_id
        self.parent_id = entity.parent_id
        self.active =  entity.active
        self.geonames_id = entity.geonames_id
    
    def to_entity(self, *, include_continent: bool = True, include_regions: bool = True, include_parent: bool = True,  include_children: bool = False) -> CountryEntity:
        return CountryEntity(
            id=self.id,
            code=self.code,
            name=self.default_name,
            continent_id=self.continent_id,
            parent_id=self.parent_id,
            active=self.active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            geonames_id=self.geonames_id,

            continent=self.continent.to_entity() if include_continent and self.continent else None,
            regions=[region.to_entity() for region in self.regions] if include_regions else [],
            parent=self.parent.to_entity() if include_parent and self.parent else None,
            children=[child.to_entity() for child in self.children] if include_children else [],
        )
