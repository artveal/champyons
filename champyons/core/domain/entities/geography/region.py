from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .nation import Nation

@dataclass
class Region(ActiveMixin, GeographyMixin, TimestampMixin):
    """ A supranational"""
    id: Optional[int] = None
    name: str = ""

    # Relationships
    nations: List["Nation"] = field(default_factory=list)