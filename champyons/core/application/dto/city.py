from typing import Optional
from pydantic import BaseModel, Field, PositiveInt
from datetime import datetime
from champyons.core.domain.enums.city import CityPopulationRange

from .translation import TranslationRead
from .nation import NationRead
from .local_region import LocalRegionRead

from pydantic_extra_types.coordinate import Latitude, Longitude            

class CityBase(BaseModel):
    default_name: str
    nation_id: PositiveInt
    local_region_id: PositiveInt

    population_range: Optional[CityPopulationRange] = None
    latitude: Optional[Latitude] = None
    longitude: Optional[Longitude] = None
    altitude: Optional[PositiveInt] = None

    geonames_id: Optional[PositiveInt] = None

    model_config = {
        "use_enum_values": True
    }
 
class CityCreate(CityBase):
    created_by_id: Optional[PositiveInt] = None

class CityUpdate(CityBase):
    default_name: Optional[str] = None
    nation_id: Optional[PositiveInt] = None
    local_region_id: Optional[PositiveInt] = None

    population_range: Optional[CityPopulationRange] = None
    latitude: Optional[Latitude] = None
    longitude: Optional[Longitude] = None
    altitude: Optional[PositiveInt] = None

    geonames_id: Optional[PositiveInt] = None

    active: Optional[bool] = None
    deactivated_at: Optional[datetime] = None
    updated_by_id: Optional[PositiveInt] = None

class CityRead(CityBase):
    id: PositiveInt

    nation: Optional[NationRead] = None
    local_region: Optional[LocalRegionRead] = None

    active: bool
    deactivated_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[PositiveInt] = None
    updated_by_id: Optional[PositiveInt] = None

    name_translations: list[TranslationRead] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }