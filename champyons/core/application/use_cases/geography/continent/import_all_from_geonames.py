# core/application/use_cases/geography/import_all_continents_from_geonames.py
from champyons.core.ports.services.geonames_service import GeonamesRepository
from champyons.core.application.use_cases.geography.continent.create_from_geonames import (
    CreateContinentFromGeonames
)
from champyons.core.application.dto.continent import ContinentRead

class ImportAllContinentsFromGeonames:
    """
    Use Case: Import all continents from geonames
    
    Reuses CreateContinentFromGeonames for each continent.
    """
    
    def __init__(
        self,
        geonames_repo: GeonamesRepository,
        create_continent_uc: CreateContinentFromGeonames
    ):
        self.geonames = geonames_repo
        self.create_continent = create_continent_uc
    
    def execute(self) -> list[ContinentRead]:
        """
        Import all continents from Geonames.
        
        Returns:
            List of created continents
        """
        # 1. Search all continents in Geonames todos los continentes en Geonames
        geo_data_list = self.geonames.search_by_query(
            fcode="CONT",
        )
        
        # 2. Create each continent
        created_continents = []
        for geo_data in geo_data_list:
            try:
                continent = self.create_continent.execute(geo_data.geonames_id)
                created_continents.append(continent)
            except Exception as e:
                # Log error but continue with next
                print(f"Error creating continent {geo_data.name}: {e}")
        
        return created_continents