from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.enums.region import RegionTypeEnum

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .nation import Nation

@dataclass
class Region(ActiveMixin, GeographyMixin, TimestampMixin):
    """ A supranational entity thar contains nations. Can be used for geographics regions, treaties..."""
    id: Optional[int] = None
    name: str = ""
    type: RegionTypeEnum = RegionTypeEnum.SCOUTABLE_REGION

    # Relationships
    nations: List["Nation"] = field(default_factory=list)