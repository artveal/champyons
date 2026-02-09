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
    from .nationality import Nationality

@dataclass
class Country(GeographyMixin, TimestampMixin, ActiveMixin):
    """ Represents a country (e.g. United Kingdom, Spain, Argentina...)"""
    id: Optional[int] = None
    code: str = ""
    name: str = ""

    continent_id: int|None = None
    parent_id: int|None = None

    # Optional relations for domain use
    nationality: Optional["Nationality"] = None
    continent: Optional["Continent"] = None
    regions: List["Region"] = field(default_factory=list)
    parent: Optional["Country"] = None

    children: List["Country"] = field(default_factory=list)
    cities: List["City"] = field(default_factory=list)
    local_regions: List["LocalRegion"] = field(default_factory=list)

    @property
    def region(self) -> "Region"|None:
        for r in self.regions:
            if r.type.value == "SCOUTABLE_REGION":
                return r