from dataclasses import dataclass, field
from typing import List, Optional

from .mixins.geography import GeographyMixin
from .mixins.timestamp import TimestampMixin
from .mixins.active import ActiveMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation

@dataclass
class Region(ActiveMixin, GeographyMixin, TimestampMixin):
    id: Optional[int] = None
    name: str = ""

    # Relationships
    nations: List["Nation"] = field(default_factory=list)