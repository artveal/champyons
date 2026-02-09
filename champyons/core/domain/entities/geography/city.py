from champyons.core.domain.entities.mixins.author import AuthorMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.enums.city import CityPopulationRange

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .continent import Continent
    from .country import Country
    from .local_region import LocalRegion

@dataclass
class City(AuthorMixin, ActiveMixin, GeographyMixin, TimestampMixin):
    ''' Represents a city or town'''
    id: Optional[int] = None
    name: str = ""
    population_range: CityPopulationRange = CityPopulationRange.UNSET
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[int] = None

    # Foreign keys
    nation_id: Optional[int] = None
    local_region_id: Optional[int] = None

    # Optional domain references
    nation: Optional["Country"] = None
    local_region: Optional["LocalRegion"] = None

    @property
    def population(self) -> int|None:
        if self.population_range.name == "UNSET": 
            return
        min_pop = self.population_range.min_population
        max_pop = self.population_range.max_population or min_pop
        
        return (max_pop+min_pop)//2
    
    @property
    def continent(self) -> "Continent"|None:
        if hasattr(self.nation, "continent"):
            return self.nation.continent
    
    def update_population(self, new_population: int) -> None:
        self.population_range = CityPopulationRange.from_population(new_population)
    




