from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .nation import Nation
    from .city import City

@dataclass
class LocalRegion(ActiveMixin, GeographyMixin, TimestampMixin):
    """ Represents a subnational region of a country. It might be an administrative region
    or a geographical region inside a country (e.g. a county). """
    id: Optional[int] = None
    name: str = ""

    # Foreign Keys
    nation_id: Optional[int] = None
    parent_local_region_id: Optional[int] = None
    other_nationality_id: Optional[int] = None

    # Relationships
    nation: Optional["Nation"] = None
    cities: List["City"] = field(default_factory=list)
    other_nationality: Optional["Nation"] = None

    # Self-referential
    parent: Optional["LocalRegion"] = None
    children: List["LocalRegion"] = field(default_factory=list)
