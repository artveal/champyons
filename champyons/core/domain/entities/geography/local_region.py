from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .continent import Continent
    from .nation import Nation
    from .city import City
    from .nationality import Nationality

@dataclass
class LocalRegion(ActiveMixin, GeographyMixin, TimestampMixin):
    """ Represents a subnational region of a country. It might be an administrative region
    or a geographical region inside a country (e.g. England (UK), Andalusia (Spain)..). """
    id: Optional[int] = None
    name: str = ""

    # Foreign Keys
    nation_id: Optional[int] = None
    parent_local_region_id: Optional[int] = None

    # Relationships
    nationality: Optional["Nationality"] = None
    nation: Optional["Nation"] = None
    _cities: List["City"] = field(default_factory=list) # List of cities that depend directly on the local_region (excluding children)

    immigration_rate: Optional[float] = None # Percentaje of foreigners (0.10 means that 10% of the population is an inmigrant)
    foreign_distribution: dict["Nationality", float] = field(default_factory=dict) # Distribution of foreign nationalities (e.g. {Nationality.ITALY: 0.5, Nationality:FRANCE: 0.5)

    # Self-referential
    parent: Optional["LocalRegion"] = None
    children: List["LocalRegion"] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_immigration_data()

    @property
    def cities(self) -> List["City"]:
        all_cities = self._cities
        for child in self.children:
            all_cities.extend(child.cities)
        return all_cities
    
    @property
    def continent(self) -> Continent|None:
        if hasattr(self.nation, "continent"):
            return self.nation.continent
    
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
                
    def get_parents(self) -> List["LocalRegion"]:
        " Returns a list of all parent local regions, sorted by hierarchy (from lower to higher)"
        parents = [self.parent]
        parents.extend(self.parent.get_parents())
        return parents
    
    def get_random_nationality(self) -> "Nationality":
        """
        Returns a random nationality based on immigration rate and distribution.
        Falls back to parent or nation if no nationality is defined.
        """
        # If no nationality, delegate to parent or nation
        if self.nationality is None:
            if self.parent:
                return self.parent.get_random_nationality()
            else:
                if self.nation is None:
                    raise ValueError(f"LocalRegion {self.name} has no nationality, parent, or nation")
                return self.nation.get_random_nationality()
        
        # No immigration or indigenous roll
        if self.immigration_rate is None or self.immigration_rate == 0:
            return self.nationality
        
        # Roll for indigenous vs foreign
        if random.random() > self.immigration_rate:
            return self.nationality  # Indigenous
        else:
            # Foreign nationality
            if not self.foreign_distribution:
                # Fallback to indigenous if foreign_distribution somehow empty
                return self.nationality
            
            nationalities = list(self.foreign_distribution.keys())
            weights = list(self.foreign_distribution.values())
            return random.choices(nationalities, weights=weights, k=1)[0]
        
    def is_indigenous_nationality(self, nationality: "Nationality") -> bool:
        """Check if a nationality is indigenous to this nation."""
        return self.nationality == nationality
    
    
