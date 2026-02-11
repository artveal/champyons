from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .continent import Continent
    from .country import Country
    from .city import City
    from .nationality import Nationality

@dataclass
class LocalRegion(ActiveMixin, GeographyMixin, TimestampMixin):
    """ Represents a subnational region of a country. It might be an administrative region
    or a geographical region inside a country (e.g. England (UK), Andalusia (Spain)..). """
    id: Optional[int] = None
    name: str = field(default="")
    code: Optional[str] = None

    # Foreign Keys
    country_id: Optional[int] = None
    parent_local_region_id: Optional[int] = None

    # Relationships
    nationality: Optional["Nationality"] = None
    country: Optional["Country"] = None
    _cities: List["City"] = field(default_factory=list) # List of cities that depend directly on the local_region (excluding children)

    # Self-referential
    parent: Optional["LocalRegion"] = None
    children: List["LocalRegion"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.nationality and (not self.code or not self.name.strip()):
            raise ValueError("Local Region code cannot be empty if represents a nationality") 
        if not self.name or not self.name.strip():
            raise ValueError("Local Region name cannot be empty") 
        
    @property
    def cities(self) -> List["City"]:
        all_cities = list(self._cities)
        for child in self.children:
            all_cities.extend(child.cities)
        return all_cities
    
    @property
    def continent(self) -> Continent|None:
        if self.country:
            return self.country.continent

    @property               
    def parents(self) -> List["LocalRegion"]:
        " Returns a list of all parent local regions, sorted by hierarchy (from lower to higher)"
        parents = list()
        if self.parent:
            parents.append(self.parent)
            parents.extend(self.parent.parents)
        return parents
    
    
    
