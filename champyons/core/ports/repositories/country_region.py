from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.entities.geography import Country, Region

class NationRegionRepository(ABC):
    @abstractmethod
    def add_country_to_region(self, country_id: int, region_id: int) -> None:
        """
        Adds a country to a region

        """

    @abstractmethod
    def remove_country_from_region(self, country_id: int, region_id: int) -> None:
        """
        Removes a country from a region.
        """

    @abstractmethod
    def get_regions_for_country(self, country_id: int) -> List[Region]:
        """
        Retrieve all regions that a country belongs to
        """

    @abstractmethod
    def get_countries_for_region(self, region_id: int) -> List[Country]:
        """
        Retrive all countries that belong to a region
        """