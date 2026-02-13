from .region import RegionRead
from .continent import ContinentRead
from .country import NationRead

RegionRead.model_rebuild()
NationRead.model_rebuild()
ContinentRead.model_rebuild()

