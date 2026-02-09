from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.geography.nationality import Nationality
from .base import BaseRepository

class NationalityRepository(BaseRepository[Nationality], ABC):      
    @abstractmethod
    def get_by_continent_id(self, continent_id: int) -> List[Nationality]:
        """
        Retrieve all nationalities that belong to a specific continent.
        """