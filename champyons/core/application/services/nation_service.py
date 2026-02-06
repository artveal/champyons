from champyons.core.repositories.nation import NationRepository
from champyons.core.repositories.continent import ContinentRepository
from champyons.core.services.translation_service import TranslationService
from champyons.core.domain.entities.geography.nation import Nation as NationEntity
from champyons.core.adapters.geonames.geonames import parse_from_geonames_id
from champyons.schemas.nation import NationCreate, NationUpdate, NationRead

class NationService:
    def __init__(self, nation_repository: NationRepository, continent_repository: ContinentRepository, translation_service: TranslationService):
        self._nation_repo = nation_repository
        self._continent_repo = continent_repository
        self.translation_service = translation_service

    def create(self, data: NationCreate) -> NationRead:
        entity = NationEntity(
            code=data.code,
            name=data.default_name,
            is_world_federation_member=data.is_world_federation_member,
            is_confederation_member=data.is_confederation_member,
            continent_id=data.continent_id,
            parent_id=data.parent_id,
            active=data.active,
            geonames_id=data.geonames_id,
        )

        saved = self._nation_repo.save(entity)

        # Manage translations
        self._set_translations(saved, data)

        return self._to_read_model(saved)
    
    def create_from_geonames(self, geonames_id: int, geonames_username: str, geonames_lang: str|None = None, is_world_federation_member: bool = True, is_confederation_member: bool = True) -> NationRead:
        result = parse_from_geonames_id(
            username=geonames_username,
            geonames_id=geonames_id,
            lang=geonames_lang
        )

        if result.fcl.value != "a":
            raise ValueError(f"Given geonames_id ({geonames_id}) does not correspond to a nation, but {result.fcl.value}") 

        code = result.countryCode
        assert code, "Nation does not have code. Strange, innit?"
        name = result.name
        geonames_id = result.geonameId
        continent = self._continent_repo.get_by_code(result.continentCode) if result.continentCode else None
        continent_id = continent.id if continent else None
        translation_languages = {"en", "es", "it"} # TO-DO: list of available langs must be returned by system
        translations = {key: "" for key in translation_languages}

        for alternate_name in result.alternateNames:
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
                    
        
        translated_names = [{"language": l, "translation": t} for l, t in translations.items() if t]

        return self.create(NationCreate(
            default_name=name,
            code=code,
            geonames_id=geonames_id,
            continent_id=continent_id,
            is_world_federation_member=is_world_federation_member,
            is_confederation_member=is_confederation_member,
            translated_names=translated_names
        ))

    # --------------------
    # Update
    # --------------------
    def update(self, nation_id: int, data: NationUpdate) -> NationRead:
        entity = self._nation_repo.get_by_id(nation_id)
        if not entity:
            raise ValueError("Nation not found")
        
        updates = data.model_dump(exclude_unset=True)

        # map name changes between pydantic model NationUpdate and domain entity model Nation
        FIELD_MAP = {
            "default_name": "name",
        }

        for field, value in updates.items():
            # translations must be handled separetely
            if field.endswith("_translations"):
                continue

            entity_field = FIELD_MAP.get(field, field)
            setattr(entity, entity_field, value)

        updated = self._nation_repo.save(entity)

        # handle translation changes:
        self._set_translations(updated, data)
        
        return self._to_read_model(updated)

    # --------------------
    # Read
    # --------------------
    def get_by_id(self, nation_id: int) -> NationRead:
        entity = self._nation_repo.get_by_id(nation_id)
        if not entity:
            raise ValueError("Nation not found")

        return self._to_read_model(entity)
    
    def get_by_code(self, code: str) -> NationRead:
        entity = self._nation_repo.get_by_code(code)
        if not entity:
            raise ValueError("Nation not found")
        
        return self._to_read_model(entity)

    def get_by_continent(self, continent_id: int) -> list[NationRead]:
        nations = self._nation_repo.get_by_continent_id(continent_id)
        return [self._to_read_model(n) for n in nations]

    # --------------------
    # Delete
    # --------------------
    def delete(self, nation_id: int) -> None:
        entity = self._nation_repo.get_by_id(nation_id)
        if not entity:
            raise ValueError("Nation not found")

        self._nation_repo.delete(entity)

    # --------------------
    # Mapping
    # --------------------
    def _to_read_model(self, entity: NationEntity, *, include_contienent: bool = True, include_region: bool = True, include_parent: bool = True, include_children: bool = False) -> NationRead:
        schema = NationRead.from_entity(entity, include_continent=include_contienent, include_region=include_region, include_parent=include_parent, include_children=include_children)
        return schema
    
    def _set_translations(self, entity: NationEntity, input_data: NationCreate|NationUpdate) -> None:
        if entity.id:
            self.translation_service.set_translations(entity="nation", foreign_key=entity.id, field_name="name", translations=getattr(input_data, "name_translations"), use_index=False)
            self.translation_service.set_translations(entity="nation", foreign_key=entity.id, field_name="denonyms", translations=getattr(input_data, "denonym_translations"), use_index=True)

        