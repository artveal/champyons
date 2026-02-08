from champyons.core.ports.repositories.nation import NationRepository
from champyons.core.application.services.translation_service import TranslationService
from champyons.core.domain.entities.geography.nation import Nation as NationEntity
from champyons.core.application.dto.nation import NationCreate, NationUpdate, NationRead

class NationService:
    def __init__(self, nation_repository: NationRepository, translation_service: TranslationService):
        self.nation_repo = nation_repository
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

        saved = self.nation_repo.save(entity)

        # Manage translations
        self._set_translations(saved, data)

        return self._to_read_model(saved)

    # --------------------
    # Update
    # --------------------
    def update(self, nation_id: int, data: NationUpdate) -> NationRead:
        entity = self.nation_repo.get_by_id(nation_id)
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

        updated = self.nation_repo.save(entity)

        # handle translation changes:
        self._set_translations(updated, data)
        
        return self._to_read_model(updated)

    # --------------------
    # Read
    # --------------------
    def get_by_id(self, nation_id: int) -> NationRead:
        entity = self.nation_repo.get_by_id(nation_id)
        if not entity:
            raise ValueError("Nation not found")

        return self._to_read_model(entity)
    
    def get_by_code(self, code: str) -> NationRead:
        entity = self.nation_repo.get_by_code(code)
        if not entity:
            raise ValueError("Nation not found")
        
        return self._to_read_model(entity)

    def get_by_continent(self, continent_id: int) -> list[NationRead]:
        nations = self.nation_repo.get_by_continent_id(continent_id)
        return [self._to_read_model(n) for n in nations]

    # --------------------
    # Delete
    # --------------------
    def delete(self, nation_id: int) -> None:
        entity = self.nation_repo.get_by_id(nation_id)
        if not entity:
            raise ValueError("Nation not found")

        self.nation_repo.delete(entity)

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

        