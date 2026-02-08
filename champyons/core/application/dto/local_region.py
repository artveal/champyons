from typing import Optional, List, Final
from pydantic import BaseModel, field_validator, PositiveInt
from datetime import datetime

from champyons.core.application.dto.nation import NationRead
from champyons.core.application.dto.city import CityRead

ForeignKey = PositiveInt

MAX_LOCAL_REGION_LEVEL: Final[int] = 3

class LocalRegionBase(BaseModel):
    default_name: str
    nation_id: ForeignKey
    parent_local_region_id: ForeignKey
    other_nationality_id: ForeignKey

    geonames_id: Optional[PositiveInt] = None
  
class LocalRegionCreate(LocalRegionBase):
    created_by_id: Optional[ForeignKey] = None

class LocalRegionUpdate(LocalRegionBase):
    default_name: Optional[str] = None
    nation_id: Optional[ForeignKey] = None
    parent_local_region_id: Optional[ForeignKey] = None
    geonames_id: Optional[PositiveInt] = None

    active: Optional[bool] = None
    deactivated_at: Optional[datetime] = None
    updated_by_id: Optional[ForeignKey] = None

class LocalRegionRead(LocalRegionBase):
    id: PositiveInt
    nation: Optional["NationRead"] = None
    parent: Optional["LocalRegionRead"] = None

    active: bool
    deactivated_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[ForeignKey] = None
    updated_by_id: Optional[ForeignKey] = None

    model_config = {
        "from_attributes": True
    } 



