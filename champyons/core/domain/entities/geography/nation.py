from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .continent import Continent
    from .region import Region
    from .local_region import LocalRegion
    from .city import City

@dataclass
class Nation(GeographyMixin, TimestampMixin, ActiveMixin):
    """ Represents a country, a national entity (such as England, Scotland...) or
    any entity that might represent a nationality """
    id: Optional[int] = None
    code: str = ""
    name: str = ""

    is_world_federation_member: bool = True
    is_confederation_member: bool = False

    continent_id: int|None = None
    parent_id: int|None = None

    # Optional relations for domain use
    continent: Optional["Continent"] = None
    regions: List["Region"] = field(default_factory=list)
    parent: Optional["Nation"] = None

    children: List["Nation"] = field(default_factory=list)
    cities: List["City"] = field(default_factory=list)
    local_regions: List["LocalRegion"] = field(default_factory=list)