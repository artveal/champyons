from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.enums.nationality import NationalityEntityType
from champyons.core.domain.value_objects.geography.culture import CultureDistribution
from champyons.core.domain.value_objects.geography.nationality_rules import NationalityRules

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .nation import Nation
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
    entity: Optional[Nation|LocalRegion] = None

    is_club_nation_base: bool = True
    is_world_federation_member: bool = True
    is_confederation_member: bool = False

    nationality_rules: Optional[NationalityRules] = None
    culture_distribution: Optional[CultureDistribution] = None 

    @property
    def name(self) -> str:
        return self.entity.name
    
    @property
    def local_regions(self) -> List[LocalRegion]:
        return self.entity.local_regions if isinstance(self.entity, Nation) else self.entity.children
    
    @property
    def cities(self) -> List[City]:
        return self.entity.cities
