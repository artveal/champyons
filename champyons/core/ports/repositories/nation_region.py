from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.geography import Nation, Region

class NationRegionRepository(ABC):
    @abstractmethod
    def add_nation_to_region(self, nation_id: int, region_id: int) -> None:
        ...

    @abstractmethod
    def remove_nation_from_region(self, nation_id: int, region_id: int) -> None:
        ...

    @abstractmethod
    def get_regions_for_nation(self, nation_id: int) -> List[Region]:
        ...

    @abstractmethod
    def get_nations_for_region(self, region_id: int) -> List[Nation]:
        ...