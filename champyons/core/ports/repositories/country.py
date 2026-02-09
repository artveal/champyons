from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.geography.country import Country
from .base import BaseRepository

class NationRepository(BaseRepository[Country], ABC):
    @abstractmethod
    def get_by_code(self, code: str) -> Country: 
        """
        Retrieve a country by its code, usually the ISO 3166-1 alpha-2 code
        """
        
    @abstractmethod
    def get_by_continent_id(self, continent_id: int) -> List[Country]:
        """
        Retrieve all countries that belong to a specific continent.
        """

    @abstractmethod
    def get_by_geonames_id(self, geonames_id: int) -> Country:
        """ 
        Retrieve a country by its geonames ID 
        """