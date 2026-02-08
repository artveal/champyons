from champyons.core.ports.repositories.continent import ContinentRepository
from champyons.core.domain.entities.geography.continent import Continent as ContinentEntity
from champyons.core.application.dto.continent import ContinentCreate, ContinentUpdate, ContinentRead
from champyons.core.application.services.translation_service import TranslationService

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