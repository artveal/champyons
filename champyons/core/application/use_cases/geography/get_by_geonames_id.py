from champyons.core.ports.repositories.continent import ContinentRepository
from champyons.core.ports.repositories.region import RegionRepository
from champyons.core.ports.repositories.country import NationRepository
from champyons.core.ports.repositories.local_region import LocalRegionRepository
from champyons.core.ports.repositories.city import CityRepository
from champyons.core.application.dto.continent import ContinentRead
from champyons.core.application.dto.region import RegionRead
from champyons.core.application.dto.country import NationRead
from champyons.core.application.dto.local_region import LocalRegionRead
from champyons.core.application.dto.city import CityRead

type GeoRead = ContinentRead | RegionRead | NationRead | LocalRegionRead | CityRead

class GetGeographicByGeonamesId:
    """
    Use Case: Search in persisted data for any geography object with given geonames id.

    If two or more entities share geonames id, only one instance will be return following this priority:
    City > LocalRegion > Nation > Region > Continent
    
    Responsabilities:
    - Fetch data from Geonames (via port)
    - Validate that the data is a continent
    - Process tranlations
    - Delegate creation to ContinentService
    """
    
    def __init__(
        self,
        continent_repo: ContinentRepository,
        region_repo: RegionRepository,
        nation_repo: NationRepository,
        local_region_repo: LocalRegionRepository,
        city_repo: CityRepository
    ):
        self.continent_repo = continent_repo
        self.region_repo = continent_repo
        self.continent_repo = region_repo
        self.nation_repo = nation_repo
        self.local_region_repo = local_region_repo
        self.city_repo = city_repo
    
    def execute(self, geonames_id: int) -> GeoRead|None:
        """
        Create continent from Geonames ID.
        
        Args:
            geonames_id: ID from Geonames
            
        Returns:
            ContinentRead, RegionRead or NationRead with given id or None, if it is not found
            
        """
        # 1. Try cities
        geo_data = self.city_repo.get_by_geonames_id(geonames_id)
        
        # 2. Try local regions
        if not geo_data:
            geo_data = self.local_region_repo.get_by_geonames_id(geonames_id)

        # 3. Try local regions
        if not geo_data:
            geo_data = self.nation_repo.get_by_geonames_id(geonames_id)

        # 4. Try local regions
        if not geo_data:
            geo_data = self.region_repo.get_by_geonames_id(geonames_id)

        # 5. Try local regions
        if not geo_data:
            geo_data = self.continent_repo.get_by_geonames_id(geonames_id)

        return geo_data