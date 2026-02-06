from typing import Optional, List
from pydantic import BaseModel, Field, PositiveInt
from datetime import datetime
from ..core.domain.enums.city import CityPopulationRange

from .translation import TranslationRead
from .nation import NationRead
from .local_region import LocalRegionRead

from pydantic_extra_types.coordinate import Latitude, Longitude            

ForeignKey = PositiveInt

class CityBase(BaseModel):
    default_name: str
    nation_id: ForeignKey
    local_region_id: ForeignKey

    population_range: Optional[CityPopulationRange] = None
    latitude: Optional[Latitude] = None
    longitude: Optional[Longitude] = None
    altitude: Optional[PositiveInt] = None

    geonames_id: Optional[PositiveInt] = None

    model_config = {
        "use_enum_values": True
    }
 
class CityCreate(CityBase):
    created_by_id: Optional[ForeignKey] = None

class CityUpdate(CityBase):
    default_name: Optional[str] = None
    nation_id: Optional[ForeignKey] = None
    local_region_id: Optional[ForeignKey] = None

    population_range: Optional[CityPopulationRange] = None
    latitude: Optional[Latitude] = None
    longitude: Optional[Longitude] = None
    altitude: Optional[PositiveInt] = None

    geonames_id: Optional[PositiveInt] = None

    active: Optional[bool] = None
    deactivated_at: Optional[datetime] = None
    updated_by_id: Optional[ForeignKey] = None

class CityRead(CityBase):
    id: PositiveInt

    nation: Optional[NationRead] = None
    local_region: Optional[LocalRegionRead] = None

    active: bool
    deactivated_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[ForeignKey] = None
    updated_by_id: Optional[ForeignKey] = None

    name_translations: list[TranslationRead] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }