from champyons.core.repositories.continent import ContinentRepository
from champyons.core.domain.entities.continent import Continent as ContinentEntity
from champyons.core.generator.geonames import parse_from_geonames_id, parse_from_geonames_search, GeonamesResult
from champyons.schemas.continent import ContinentCreate, ContinentUpdate, ContinentRead
from champyons.core.services.translation_service import TranslationService

class ContinentService:
    def __init__(self, continent_repostory: ContinentRepository, translation_service: TranslationService):
        self._continent_repo = continent_repostory
        self.translation_service = translation_service

    def create(self, data: ContinentCreate) -> ContinentRead:
        entity = ContinentEntity(
            code=data.code,
            name=data.default_name,
            geonames_id=data.geonames_id,
            active=data.active
        )

        saved = self._continent_repo.save(entity)

        # Manage translations
        self._set_translations(saved, data)

        return self._to_read_model(saved)
    
    def _create_from_geonames(self, geonames_result: GeonamesResult) -> ContinentRead:
        if geonames_result.fcode.value != "cont":
            raise ValueError(f"Given geonames_id ({geonames_result.geonameId}) does not correspond to a continent, but fcode={geonames_result.fcode.value}") 

        code = geonames_result.continentCode
        assert code, "Continent does not have code. Strange, innit?"
        name = geonames_result.name
        geonames_id = geonames_result.geonameId
        translation_languages = {"en", "es", "it"} # TO-DO: list of available langs must be returned by system
        translations = {key: "" for key in translation_languages}

        for alternate_name in geonames_result.alternateNames:
            if not alternate_name.lang:
                continue
            if alternate_name.lang in translation_languages:
                if translations.get(alternate_name.lang, "") == "":
                    translations[alternate_name.lang] = alternate_name.name
                elif alternate_name.isPreferredName:
                    translations[alternate_name.lang] = alternate_name.name
                    translation_languages.remove(alternate_name.lang)
                elif alternate_name.isShortName:
                    translations[alternate_name.lang] = alternate_name.name
                    
        
        translated_names = [{"language": l, "translation": t} for l, t in translations.items() if t and t != name]

        return self.create(ContinentCreate(
            default_name=name,
            code=code,
            geonames_id=geonames_id,
            translated_names=translated_names
        ))

    def create_all_from_geonames(self, geonames_username: str, geonames_lang: str|None = None) -> list[ContinentRead]:
        continents = list()
        for result in parse_from_geonames_search(username=geonames_username, lang=geonames_lang, fcode="CONT"):
            continents.append(self._create_from_geonames(result))

        return continents
    
    def create_from_geonames_id(self, geonames_id: int, geonames_username: str, geonames_lang: str|None = None) -> ContinentRead:
        result = parse_from_geonames_id(
            username=geonames_username,
            geonames_id=geonames_id,
            lang=geonames_lang
        )

        return self._create_from_geonames(result)

        
    
    def update(self, continent_id: int, data: ContinentUpdate) -> ContinentRead:
        entity = self._continent_repo.get_by_id(continent_id)
        if not entity:
            raise ValueError("Continent not found")
        
        updates = data.model_dump(exclude_unset=True)

        # map name changes between pydantic model ContinentUpdate and domain entity model Continent
        FIELD_MAP = {
            "default_name": "name",
        }

        for field, value in updates.items():
            # translations must be handled separetely
            if field.endswith("_translations"):
                continue

            entity_field = FIELD_MAP.get(field, field)
            setattr(entity, entity_field, value)

        updated = self._continent_repo.save(entity)
        
        # handle translation changes:
        self._set_translations(updated, data)

        return self._to_read_model(updated)
    
    def get_by_id(self, continent_id: int) -> ContinentRead:
        entity = self._continent_repo.get_by_id(continent_id)
        if not entity:
            raise ValueError("Continent not found")
        
        return self._to_read_model(entity)
    
    def delete(self, continent_id: int):
        entity = self._continent_repo.get_by_id(continent_id)
        if not entity:
            raise ValueError("Continent not found")
        
        self._continent_repo.delete(entity)
    
    def _to_read_model(self, entity: ContinentEntity, include_nations: bool = False) -> ContinentRead:
        schema = ContinentRead.from_entity(entity, include_nations=include_nations)
        return schema
    
    def _set_translations(self, entity: ContinentEntity, input_data: ContinentCreate|ContinentUpdate) -> None:
        if entity.id:
            self.translation_service.set_translations(entity="continent", foreign_key=entity.id, field_name="name", translations=getattr(input_data, "name_translations"), use_index=False)
        
        