from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.region import Region
from .base import BaseRepository

class RegionRepository(BaseRepository[Region], ABC):
    pass