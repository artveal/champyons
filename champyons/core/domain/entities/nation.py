from dataclasses import dataclass, field
from typing import List, Optional

from .mixins.geography import GeographyMixin
from .mixins.timestamp import TimestampMixin
from .mixins.active import ActiveMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .continent import Continent
    from .region import Region
    from .local_region import LocalRegion
    from .city import City

@dataclass
class Nation(GeographyMixin, TimestampMixin, ActiveMixin):
    id: Optional[int] = None
    code: str = ""
    name: str = ""

    is_world_federation_member: bool = True
    is_confederation_member: bool = False

    continent_id: int|None = None
    region_id: int|None = None
    parent_id: int|None = None

    # Optional relations for domain use
    continent: Optional["Continent"] = None
    region: Optional["Region"] = None
    parent: Optional["Nation"] = None

    children: List["Nation"] = field(default_factory=list)
    cities: List["City"] = field(default_factory=list)
    local_regions: List["LocalRegion"] = field(default_factory=list)