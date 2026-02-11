from champyons.core.domain.entities.mixins.author import AuthorMixin
from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.enums.city import CityPopulationRange

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .continent import Continent
    from .country import Country
    from .local_region import LocalRegion

@dataclass
class City(AuthorMixin, ActiveMixin, GeographyMixin, TimestampMixin):
    ''' Represents a city or town'''
    id: Optional[int] = None
    name: str = field(default="")
    population_range: CityPopulationRange = CityPopulationRange.UNSET
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[int] = None

    # Foreign keys
    country_id: int = 0
    local_region_id: Optional[int] = None

    # Optional domain references
    country: Optional["Country"] = None
    local_region: Optional["LocalRegion"] = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("City name cannot be empty") 
        
        # A city must belong to a country
        if self.country_id <= 0:
            raise ValueError(f"City '{self.name}' must belong to a country")
        
        # Validate coordinates (if defined)
        if self.latitude and not(-90 <= self.latitude <= 90):
            raise ValueError(
                f"Invalid latitude for city '{self.name}': {self.latitude}. "
                f"Must be between -90 and 90."
            )
        
        if self.longitude and not(-180 <= self.longitude <= 180):
            raise ValueError(
                f"Invalid longitude for city '{self.name}': {self.longitude}. "
                f"Must be between -180 and 180."
            )

    @property
    def population(self) -> int|None:
        min_pop = self.population_range.min_population
        if min_pop is not None:
            max_pop = self.population_range.max_population or min_pop
            return (max_pop+min_pop)//2
    
    @property
    def continent(self) -> Continent|None:
        if self.country:
            return self.country.continent
    
    def update_population(self, new_population: int) -> None:
        self.population_range = CityPopulationRange.from_population(new_population)
    




