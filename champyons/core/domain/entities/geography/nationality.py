from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.enums.nationality import NationalityEntityType
from champyons.core.domain.value_objects.geography.culture import CultureDistribution
from champyons.core.domain.value_objects.geography.nationality_rules import NationalityRules

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from champyons.core.ports.repositories.nationalities import NationalityRepository
    from .continent import Continent
    from .country import Country
    from .local_region import LocalRegion
    from .city import City

@dataclass
class Nationality(TimestampMixin, ActiveMixin):
    """
    Represents any entity that may have a national team. Nations and LocaL Regions are elegible
    to have a nationality (e.g. England (local region), Germany (nation)... )
    """
    id: Optional[int] = None
    entity_type: NationalityEntityType = NationalityEntityType.COUNTRY
    entity_id: Optional[int] = None
    entity: Optional[Country|LocalRegion] = None

    is_club_nation_base: bool = True
    is_world_federation_member: bool = True
    is_confederation_member: bool = False

    nationality_rules: Optional[NationalityRules] = None
    culture_distribution: Optional[CultureDistribution] = None 
    
    immigration_rate: Optional[float] = None # Percentaje of foreigners (0.10 means that 10% of the population is an inmigrant)
    foreign_nationalities_id: List[int] = field(default_factory=list) # Foreign nationalities (e.g. {1: 0.5, 2: 0.5), 1 and 2 representing other nationalities' ids)
    
    def __post_init__(self) -> None:
        # Validar que entity_type y entity_id coinciden
        if self.entity is None or self.entity_id is None:
            raise ValueError(
                f"Entity and entity_id must be defined"
            )
        if self.entity_type == NationalityEntityType.COUNTRY:
            if not isinstance(self.entity, Country):
                raise ValueError(
                    f"Entity type is COUNTRY but entity is {type(self.entity).__name__}"
                )
        elif self.entity_type == NationalityEntityType.LOCAL_REGION:
            if not isinstance(self.entity, LocalRegion):
                raise ValueError(
                    f"Entity type is LOCAL_REGION but entity is {type(self.entity).__name__}"
                )
                
    @property
    def name(self) -> str|None:
        if self.entity:
            return self.entity.name

    @property
    def code(self) -> str | None:
        """Returns the nationality code from its associated entity."""
        if self.entity:
            return self.entity.code
        return None
        
    @property
    def local_regions(self) -> List[LocalRegion]:
        if self.entity:
            return self.entity.local_regions if isinstance(self.entity, Country) else self.entity.children
        return list()
    
    @property
    def cities(self) -> List[City]:
        if self.entity:
            return self.entity.cities
        return list()
    
    @property
    def continent(self) -> Continent|None:
        if self.entity:
            return self.entity.continent
