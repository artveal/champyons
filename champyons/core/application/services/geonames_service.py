from abc import ABC, abstractmethod
from typing import List
from champyons.core.domain.value_objects.geography.geonames import GeonamesData

class GeonamesRepository(ABC):
    @abstractmethod
    def fetch_by_id(self, geoname_id: int) -> GeonamesData:
        ...

    @abstractmethod
    def search_by_query(self, **query_params) -> List[GeonamesData]:
        ...

    @abstractmethod
    def search_children(self, nation_id: int) -> List[GeonamesData]:
        ...