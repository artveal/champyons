from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.continent import Continent
from .base import BaseRepository

class ContinentRepository(BaseRepository[Continent], ABC):
    @abstractmethod
    def get_by_code(self, code: str) -> Continent:
        pass