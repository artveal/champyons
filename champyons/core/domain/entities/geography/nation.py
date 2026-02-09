from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .continent import Continent
    from .region import Region
    from .local_region import LocalRegion
    from .city import City
    from .nationality import Nationality

@dataclass
class Nation(GeographyMixin, TimestampMixin, ActiveMixin):
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
    parent: Optional["Nation"] = None

    immigration_rate: Optional[float] = None # Percentaje of foreigners (0.10 means that 10% of the population is an inmigrant)
    foreign_distribution: dict["Nationality", float] = field(default_factory=dict) # Distribution of foreign nationalities (e.g. {Nationality.ITALY: 0.5, Nationality:FRANCE: 0.5)

    children: List["Nation"] = field(default_factory=list)
    cities: List["City"] = field(default_factory=list)
    local_regions: List["LocalRegion"] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_immigration_data()

    @property
    def region(self) -> "Region"|None:
        for r in self.regions:
            if r.type.value == "SCOUTABLE_REGION":
                return r
            
    def _validate_immigration_data(self):
        """Ensure immigration_rate and foreign_distribution are coherent."""
        if self.immigration_rate is not None:
            if not (0.0 <= self.immigration_rate <= 1.0):
                raise ValueError(
                    f"immigration_rate must be between 0 and 1, got {self.immigration_rate}"
                )
            
            if self.immigration_rate > 0 and not self.foreign_distribution:
                raise ValueError(
                    f"Nation {self.name} has immigration_rate={self.immigration_rate} "
                    "but foreign_distribution is empty"
                )
            
            if self.foreign_distribution:
                total = sum(self.foreign_distribution.values())
                if not (0.99 <= total <= 1.01):
                    raise ValueError(
                        f"foreign_distribution must sum to 1.0, got {total:.4f}"
                    )
            
    def get_random_nationality(self) -> "Nationality":
        """
        Returns a random nationality based on immigration rate and distribution.
        Falls back to parent nation if no nationality is defined.
        """
        # If no nationality, delegate to parent
        if self.nationality is None:
            if self.parent:
                return self.parent.get_random_nationality()
            else:
                raise ValueError(f"Nation {self.name} has no nationality and no parent")
        
        # No immigration or indigenous roll
        if self.immigration_rate is None or self.immigration_rate == 0:
            return self.nationality
        
        # Roll for indigenous vs foreign
        if random.random() > self.immigration_rate:
            return self.nationality  # Indigenous
        else:
            # Foreign nationality
            if not self.foreign_distribution:
                return self.nationality
            
            nationalities = list(self.foreign_distribution.keys())
            weights = list(self.foreign_distribution.values())
            return random.choices(nationalities, weights=weights, k=1)[0]
    
    def is_indigenous_nationality(self, nationality: "Nationality") -> bool:
        """Check if a nationality is indigenous to this nation."""
        return self.nationality == nationality