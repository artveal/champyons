from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.nation import Nation
from .base import BaseRepository

class NationRepository(BaseRepository[Nation], ABC):
    @abstractmethod
    def get_by_code(self, code: str) -> Nation:
        """Retrieve a nation by its code"""
        pass

    @abstractmethod
    def get_by_continent_id(self, continent_id: int) -> List[Nation]:
        """Retrieve all nations that belong to a specific continent."""
        pass
    