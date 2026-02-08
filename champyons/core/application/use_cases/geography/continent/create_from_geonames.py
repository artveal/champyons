from champyons.core.ports.services.geonames_service import GeonamesRepository, GeonamesData
from champyons.core.application.services.continent_service import ContinentService
from champyons.core.application.dto.continent import ContinentCreate, ContinentRead

class CreateContinentFromGeonames:
    """
    Use Case: Create a continent from Geonames
    
    Responsabilities:
    - Fetch data from Geonames (via port)
    - Validate that the data is a continent
    - Process tranlations
    - Delegate creation to ContinentService
    """
    
    def __init__(
        self,
        geonames_repo: GeonamesRepository,  # Port
        continent_service: ContinentService
    ):
        self.geonames = geonames_repo
        self.continent_service = continent_service
    
    def execute(self, geonames_id: int) -> ContinentRead:
        """
        Create continent from Geonames ID.
        
        Args:
            geonames_id: ID from Geonames
            
        Returns:
            ContinentRead created
            
        Raises:
            ValueError: if not valid continent
        """
        # 1. Fetch data
        geo_data = self.geonames.fetch_by_id(geonames_id)
        
        # 2. Validate it is a continent and has continent code
        if not geo_data.can_be_continent:
            raise ValueError(
                f"Geonames ID {geonames_id} is not a continent "
                f"(feature code: {geo_data.feature_code})"
            )
        
        if not geo_data.continent_code:
            raise ValueError("Continent must have a continent code")
        
        # 3. Process translations
        translations = self._process_translations(geo_data)
        
        # 4. Create DTO
        create_dto = ContinentCreate(
            code=geo_data.continent_code,
            default_name=geo_data.name,
            geonames_id=geo_data.geonames_id,
            name_translations=translations,
            active=True
        )
        
        # 6. Delegate creation to service
        return self.continent_service.create(create_dto)
    
    def _process_translations(self, geo_data: GeonamesData) -> list[dict]:
        """
        Process translations from GeonamesData.
        
        Filter and priorize from supported languages
        """
        available_languages = {"en", "es", "it", "fr", "de"}
        translations_dict = {}
        
        for lang, translation in geo_data.translations.items():
            if lang in available_languages and translation != geo_data.name:
                translations_dict[lang] = translation
        
        return [
            {"language": lang, "translation": text}
            for lang, text in translations_dict.items()
        ]