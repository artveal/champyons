from champyons.core.ports.services.geonames_service import GeonamesRepository, GeonamesData
from champyons.core.ports.repositories.continent import ContinentRepository
from champyons.core.application.services.nation_service import NationService
from champyons.core.application.dto.nation import NationCreate, NationRead

class CreateNationFromGeonames:
    """
    Use Case: Create a nation from Geonames
    
    Responsabilities:
    - Fetch data from Geonames (via port)
    - Validate that the data is a nation
    - Process translations
    - Delegate creation to NationService
    """
    
    def __init__(
        self,
        geonames_repo: GeonamesRepository,  # Port
        nation_service: NationService,
        continent_repo: ContinentRepository
    ):
        self.geonames = geonames_repo
        self.nation_service = nation_service
        self.continent_repo = continent_repo
    
    def execute(self, geonames_id: int) -> NationRead:
        """
        Create nation from Geonames ID.
        
        Args:
            geonames_id: ID from Geonames
            
        Returns:
            NationRead created
            
        Raises:
            ValueError: if not valid nation
        """
        # 1. Fetch data
        geo_data = self.geonames.fetch_by_id(geonames_id)
        
        # 2. Validate it is a continent and has a valid nation
        if not geo_data.can_be_nation:
            raise ValueError(
                f"Geonames ID {geonames_id} is not a country or a feature code that may represent an in-game nation "
                f"(feature code: {geo_data.feature_code})"
            )
        
        if not geo_data.country_code:
            raise ValueError("Nation must have a country code")
        
        # 3. Process translations
        translations = self._process_translations(geo_data)
        
        # 4. Create DTO
        create_dto = NationCreate(
            code=geo_data.country_code,
            default_name=geo_data.name,
            geonames_id=geo_data.geonames_id,
            continent_id=self.continent_repo.get_by_code(geo_data.continent_code),
            parent_id=self.nation_service._nation_repo(geo_data.other_country_codes[0]) if geo_data.other_country_codes else None,
            name_translations=translations,
            active=True
        )
        
        # 6. Delegate creation to service
        return self.nation_service.create(create_dto)
    
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