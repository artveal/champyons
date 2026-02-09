from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship      
from champyons.core.domain.entities.geography.continent import Continent as ContinentEntity
from ..base import Base
from ..mixins import ActiveMixin, GeographyMixin, TimestampMixin
from .translation import Translation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .country import Country

class Continent(Base, GeographyMixin, TimestampMixin, ActiveMixin):
    __tablename__ = "continent"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    default_name: Mapped[str] = mapped_column(String, index=True, info={"translatable": True})

    # Relationships
    countries: Mapped[list["Country"]] = relationship("Nation", back_populates="continent")

    @classmethod
    def from_entity(cls, entity: ContinentEntity) -> "Continent":
        return cls(
            id=entity.id,
            code=entity.code,
            default_name=entity.name,
            geonames_id=entity.geonames_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            active=entity.active,
        ) 
    
    def update_from_entity(self, entity: ContinentEntity):
        self.code = entity.code
        self.default_name = entity.name
        self.active = entity.active
        self.geonames_id = entity.geonames_id
        
    def to_entity(self, *, include_countrys = False) -> ContinentEntity:
        return ContinentEntity(
            id=self.id,
            code=self.code,
            name=self.default_name,
            geonames_id=self.geonames_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
            countrys=[country.to_entity() for country in self.countrys] if include_countrys else []
        )


