from champyons.core.ports.repositories.country import CountryRepository
from champyons.core.application.services.translation_service import TranslationService
from champyons.core.domain.entities.geography.country import Country as CountryEntity
from champyons.core.application.dto.country import CountryCreate, CountryUpdate, CountryRead

class CountryService:
    def __init__(self, country_repository: CountryRepository, translation_service: TranslationService):
        self.country_repo = country_repository
        self.translation_service = translation_service

    def create(self, data: CountryCreate) -> CountryRead:
        entity = CountryEntity(
            code=data.code,
            name=data.default_name,
            is_world_federation_member=data.is_world_federation_member,
            is_confederation_member=data.is_confederation_member,
            continent_id=data.continent_id,
            parent_id=data.parent_id,
            active=data.active,
            geonames_id=data.geonames_id,
        )

        saved = self.country_repo.save(entity)

        # Manage translations
        self._set_translations(saved, data)

        return self._to_read_model(saved)

    # --------------------
    # Update
    # --------------------
    def update(self, country_id: int, data: CountryUpdate) -> CountryRead:
        entity = self.country_repo.get_by_id(country_id)
        if not entity:
            raise ValueError("Country not found")
        
        updates = data.model_dump(exclude_unset=True)

        # map name changes between pydantic model CountryUpdate and domain entity model Country
        FIELD_MAP = {
            "default_name": "name",
        }

        for field, value in updates.items():
            # translations must be handled separetely
            if field.endswith("_translations"):
                continue

            entity_field = FIELD_MAP.get(field, field)
            setattr(entity, entity_field, value)

        updated = self.country_repo.save(entity)

        # handle translation changes:
        self._set_translations(updated, data)
        
        return self._to_read_model(updated)

    # --------------------
    # Read
    # --------------------
    def get_by_id(self, country_id: int) -> CountryRead:
        entity = self.country_repo.get_by_id(country_id)
        if not entity:
            raise ValueError("Country not found")

        return self._to_read_model(entity)
    
    def get_by_code(self, code: str) -> CountryRead:
        entity = self.country_repo.get_by_code(code)
        if not entity:
            raise ValueError("Country not found")
        
        return self._to_read_model(entity)

    def get_by_continent(self, continent_id: int) -> list[CountryRead]:
        countries = self.country_repo.get_by_continent_id(continent_id)
        return [self._to_read_model(n) for n in countries]

    # --------------------
    # Delete
    # --------------------
    def delete(self, country_id: int) -> None:
        entity = self.country_repo.get_by_id(country_id)
        if not entity:
            raise ValueError("Country not found")

        self.country_repo.delete(entity)

    # --------------------
    # Mapping
    # --------------------
    def _to_read_model(self, entity: CountryEntity, *, include_contienent: bool = True, include_region: bool = True, include_parent: bool = True, include_children: bool = False) -> CountryRead:
        schema = CountryRead.from_entity(entity, include_continent=include_contienent, include_region=include_region, include_parent=include_parent, include_children=include_children)
        return schema
    
    def _set_translations(self, entity: CountryEntity, input_data: CountryCreate|CountryUpdate) -> None:
        if entity.id:
            self.translation_service.set_translations(entity="country", foreign_key=entity.id, field_name="name", translations=getattr(input_data, "name_translations"), use_index=False)
            self.translation_service.set_translations(entity="country", foreign_key=entity.id, field_name="denonyms", translations=getattr(input_data, "denonym_translations"), use_index=True)

        