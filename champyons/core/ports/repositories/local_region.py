from abc import ABC, abstractmethod
from typing import List, Optional
from champyons.core.domain.entities.geography import LocalRegion
from .base import BaseRepository

class LocalRegionRepository(BaseRepository[LocalRegion], ABC):
    @abstractmethod
    def get_by_nation_id(self, nation_id: int, admin_level_depth: Optional[int] = None) -> List[LocalRegion]:
        """
        Retrieve all local regions of the given nation
        
        Params:
            - nation_id: the ID of the nation
            - admin_level_depth: if given, local regions up to this level will be retrieved. If omitted, all will be retrieved
        """
    @abstractmethod
    def get_by_geonames_id(self, geonames_id: int) -> LocalRegion:
        """ 
        Retrieve a region by its geonames ID 
        """