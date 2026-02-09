from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.geography import City
from .base import BaseRepository

class CityRepository(BaseRepository[City], ABC):
    @abstractmethod
    def get_by_country_id(self, country_id: int) -> List[City]:
        """
        Retrieve all cities of the given country
        
        Params:
            country_id: the ID of the nation
        """
    
    @abstractmethod
    def get_by_local_region_id(self, local_region_id: int, include_cities_of_children: bool = True) -> List[City]:
        """
        Retrieve all cities of the given local_region. By default, cities of the selected local region and its
        children local_regions will be retrieved. This behaviour can be changed with parameter 'include_cities_of_children'. 
        
        Params:
            local_region_id: the ID of the local_region
            include_cities_of_children : if True, retrieve all cities under this local region, whereas if False, only cities 
                that depend directly on this local region. Defaults to True
        """

    @abstractmethod
    def get_by_geonames_id(self, geonames_id: int) -> City:
        """ 
        Retrieve a region by its geonames ID 
        """