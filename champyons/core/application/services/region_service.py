from champyons.core.repositories.region import RegionRepository
from champyons.core.services.translation_service import TranslationService
from champyons.core.domain.entities.geography.region import Region as RegionEntity
from champyons.schemas.region import (
    RegionCreate,
    RegionUpdate,
    RegionRead
)

class RegionService:
    def __init__(self, region_repostory: RegionRepository, translation_service: TranslationService):
        self._region_repo = region_repostory
        self.translation_service = translation_service

    def create(self, data: RegionCreate) -> RegionRead:
        entity = RegionEntity(
            name=data.default_name,
            geonames_id=data.geonames_id,
            active=data.active
        )

        saved = self._region_repo.save(entity)

        # Manage translations
        self._set_translations(saved, data)
        
        return self._to_read_model(saved)
    
    def update(self, region_id: int, data: RegionUpdate) -> RegionRead:
        entity = self._region_repo.get_by_id(region_id)
        if not entity:
            raise ValueError("Region not found")
        
        updates = data.model_dump(exclude_unset=True)

        # map name changes between pydantic model RegionUpdate and domain entity model Region
        FIELD_MAP = {
            "default_name": "name",
        }

        for field, value in updates.items():
            # translations must be handled separetely
            if field.endswith("_translations"):
                continue

            entity_field = FIELD_MAP.get(field, field)
            setattr(entity, entity_field, value)

        updated = self._region_repo.save(entity) 

        # handle translation changes:
        self._set_translations(updated, data)

        return self._to_read_model(updated)
    
    def get_by_id(self, region_id: int) -> RegionRead:
        entity = self._region_repo.get_by_id(region_id)
        if not entity:
            raise ValueError("Region not found")
        
        return self._to_read_model(entity)
    
    def delete(self, region_id: int):
        entity = self._region_repo.get_by_id(region_id)
        if not entity:
            raise ValueError("Region not found")
        
        self._region_repo.delete(entity)

    def _to_read_model(self, entity: RegionEntity, include_nations: bool = False) -> RegionRead:
        schema = RegionRead.from_entity(entity, include_nations=include_nations)
        return schema
    
    def _set_translations(self, entity: RegionEntity, input_data: RegionCreate|RegionUpdate) -> None:
        if entity.id:
            self.translation_service.set_translations(entity="region", foreign_key=entity.id, field_name="name", translations=getattr(input_data, "name_translations"), use_index=False)
            
        
        