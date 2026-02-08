from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.geography.continent import Continent
from .base import BaseRepository

class ContinentRepository(BaseRepository[Continent], ABC):
    @abstractmethod
    def get_by_code(self, code: str) -> Continent: 
        """
        Retrieves a continent by its code
        """

    @abstractmethod
    def get_by_geonames_id(self, geonames_id: int) -> Continent:
        """
        Retrieves a continent by its geonames id
        """

