from dataclasses import dataclass, field
from typing import Optional, List

from .mixins.author import AuthorMixin
from .mixins.active import ActiveMixin
from .mixins.geography import GeographyMixin
from .mixins.timestamp import TimestampMixin

from ..enums.city import CityPopulationRange

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation
    from .local_region import LocalRegion

@dataclass
class City(AuthorMixin, ActiveMixin, GeographyMixin, TimestampMixin):
    id: Optional[int] = None
    name: str = ""
    population_range: CityPopulationRange = CityPopulationRange.UNSET
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[int] = None

    # Foreign keys
    nation_id: Optional[int] = None
    local_region_id: Optional[int] = None

    # Optional domain references
    nation: Optional["Nation"] = None
    local_region: Optional["LocalRegion"] = None