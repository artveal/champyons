from abc import ABC, abstractmethod
from typing import List, Optional
from champyons.core.domain.entities.geography import LocalRegion
from .base import BaseRepository

class LocalRegionRepository(BaseRepository[LocalRegion], ABC):
    @abstractmethod
    def get_by_country_id(self, country_id: int, admin_level_depth: Optional[int] = None) -> List[LocalRegion]:
        """
        Retrieve all local regions of the given country
        
        Params:
            - country_id: the ID of the country
            - admin_level_depth: if given, local regions up to this level will be retrieved. If omitted, all will be retrieved
        """
    @abstractmethod
    def get_by_geonames_id(self, geonames_id: int) -> LocalRegion:
        """ 
        Retrieve a region by its geonames ID 
        """