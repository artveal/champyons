from dataclasses import dataclass, field
from typing import List, Optional

from .mixins.active import ActiveMixin
from .mixins.geography import GeographyMixin
from .mixins.timestamp import TimestampMixin


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation

@dataclass
class Continent(ActiveMixin, GeographyMixin, TimestampMixin):
    id: Optional[int] = None
    code: str = ""
    name: str = ""

    # Relationships
    nations: List["Nation"] = field(default_factory=list)