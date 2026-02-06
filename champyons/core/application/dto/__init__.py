from .region import RegionRead
from .continent import ContinentRead
from .nation import NationRead

RegionRead.model_rebuild()
NationRead.model_rebuild()
ContinentRead.model_rebuild()

