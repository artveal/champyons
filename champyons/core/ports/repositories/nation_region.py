from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.geography import Nation, Region

class NationRegionRepository(ABC):
    @abstractmethod
    def add_nation_to_region(self, nation_id: int, region_id: int) -> None:
        """
        Adds a nation to a region

        """

    @abstractmethod
    def remove_nation_from_region(self, nation_id: int, region_id: int) -> None:
        """
        Removes a nation from a region.
        """

    @abstractmethod
    def get_regions_for_nation(self, nation_id: int) -> List[Region]:
        """
        Retrieve all regions that a nation belongs to
        """

    @abstractmethod
    def get_nations_for_region(self, region_id: int) -> List[Nation]:
        """
        Retrive all nations that belong to a region
        """