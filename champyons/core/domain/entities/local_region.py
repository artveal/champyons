from dataclasses import dataclass, field
from typing import List, Optional

from .mixins.geography import GeographyMixin
from .mixins.timestamp import TimestampMixin
from .mixins.active import ActiveMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation
    from .city import City

@dataclass
class LocalRegion(ActiveMixin, GeographyMixin, TimestampMixin):
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
