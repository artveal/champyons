from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.enums.region import RegionTypeEnum

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .country import Country

@dataclass
class Region(ActiveMixin, GeographyMixin, TimestampMixin):
    """ A supranational entity thar contains nations. Can be used for geographics regions, treaties..."""
    id: Optional[int] = None
    name: str = field(default="")
    type: RegionTypeEnum = RegionTypeEnum.SCOUTABLE_REGION

    # Relationships
    countries: List["Country"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Region name cannot be empty") 