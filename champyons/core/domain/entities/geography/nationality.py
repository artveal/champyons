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
    entity_type: NationalityEntityType = NationalityEntityType.NATION
    entity_id: Optional[int] = None
    entity: Optional[Country|LocalRegion] = None

    is_club_nation_base: bool = True
    is_world_federation_member: bool = True
    is_confederation_member: bool = False

    nationality_rules: Optional[NationalityRules] = None
    culture_distribution: Optional[CultureDistribution] = None 
    
    immigration_rate: Optional[float] = None # Percentaje of foreigners (0.10 means that 10% of the population is an inmigrant)
    foreign_nationalities: List["Nationality"] = field(default_factory=list) # Foreign nationalities (e.g. {Nationality.ITALY: 0.5, Nationality:FRANCE: 0.5)

    @property
    def name(self) -> str:
        return self.entity.name
    
    @property
    def local_regions(self) -> List[LocalRegion]:
        return self.entity.local_regions if isinstance(self.entity, Country) else self.entity.children
    
    @property
    def cities(self) -> List[City]:
        return self.entity.cities
    
    @property
    def continent(self) -> Continent|None:
        return self.entity.continent
    
    def get_random_nationality_for_player(
        self,
        nationality_repo: NationalityRepository
    ) -> "Nationality":
        """Generate nationality with simple foreign logic."""
        import random
        
        if random.random() < self.immigration_rate:
            # Use curated list if available
            if self.foreign_nationalities:
                foreign_id = random.choice(self.foreign_nationalities)
                foreign_nat = nationality_repo.get_by_id(foreign_id)
                if foreign_nat:
                    return foreign_nat
            
            # Fallback: same continent or all, if there is no continent
            if self.continent:
                continent_nats = nationality_repo.get_by_continent_id(self.continent.id)
            else:
                continent_nats = nationality_repo.get_all()
            if continent_nats:
                return random.choice(continent_nats)
        
        return self
