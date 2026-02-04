from pydantic import BaseModel, PositiveInt, Field, model_validator
from datetime import datetime
from collections import defaultdict

from typing import Optional, TYPE_CHECKING, Any, Union, TypeVar

from .continent import ContinentRead
from .region import RegionRead
from .translation import TranslationBase, TranslationCreate, TranslationUpdate

TTranslation = TypeVar("TTranslation", bound=TranslationBase)
TranslationInput = Union[TTranslation, dict[str, str]]

if TYPE_CHECKING:
    from .city import CityRead
    from .local_region import LocalRegionRead
    from champyons.core.domain.entities.geography.nation import Nation as NationEntity

class NationBase(BaseModel):
    default_name: str
    code: str

    continent_id: Optional[PositiveInt] = None
    region_id: Optional[PositiveInt] = None
    parent_id: Optional[PositiveInt] = None

    is_world_federation_member: bool
    is_confederation_member: bool

    # Geonames attrs
    geonames_id: Optional[PositiveInt] = None

    # Active attrs
    active: bool

class NationUpsert(BaseModel):
    translated_names: list[TranslationInput] = Field(default_factory=list, init_var=True)
    translated_denonyms: list[TranslationInput] = Field(default_factory=list, init_var=True)

    @model_validator(mode="before")
    def convert_translations(cls, values: dict[str, Any]) -> dict[str, Any]:
        raw_name_translations: list[TranslationInput] = values.get("translated_names", [])
        raw_denonym_translations: list[TranslationInput] = values.get("translated_denonyms", [])
                
        values["name_translations"] = cls._parse_translations(raw_name_translations, use_index=False)
        values["denonym_translations"] = cls._parse_translations(raw_denonym_translations, use_index=True)
        return values
    
    @staticmethod
    def _parse_translations(raw_translations: list[TranslationInput], use_index: bool = False):
        pass

class NationCreate(NationUpsert, NationBase):
    is_world_federation_member: bool = True
    is_confederation_member: bool = True

    # translations
    name_translations: list[TranslationCreate] = Field(default_factory=list, init=False)
    denonym_translations: list[TranslationCreate] = Field(default_factory=list, init=False)

    # Active attrs
    active: bool = True

    @staticmethod
    def _parse_translations(raw_translations: list[TranslationInput], use_index: bool = False) -> list:
        translations = list()
        count_by_lang = defaultdict(int)

        for item in raw_translations:
            if isinstance(item, TranslationBase):
                translations.append(item)
                continue

            lang = item["language"]
            translation = item["translation"]
            index = count_by_lang[lang] if use_index else None
            t = TranslationCreate(
                language=lang,
                translation=translation,
                index=index
            )
            translations.append(t)
            if use_index:
                count_by_lang[lang] += 1

        return translations

class NationUpdate(NationUpsert, NationBase):
    default_name: Optional[str] = None

    code: Optional[str] = None
    continent_id: Optional[PositiveInt] = None
    region_id: Optional[PositiveInt] = None
    parent_id: Optional[PositiveInt] = None

    is_world_federation_member: Optional[bool] = None
    is_confederation_member: Optional[bool] = None

    # translations
    name_translations: list[TranslationUpdate] = Field(default_factory=list, init=False)
    denonym_translations: list[TranslationUpdate] = Field(default_factory=list, init=False)

    # Active attrs
    active: Optional[bool] = None

    @staticmethod
    def _parse_translations(raw_translations: list[TranslationInput], use_index: bool = False) -> list:
        translations = list()
        count_by_lang = defaultdict(int)

        for item in raw_translations:
            if isinstance(item, TranslationBase):
                translations.append(item)
                continue

            lang: str = item["language"]
            translation: str = item["translation"]

            if "index" in item:
                index = int(item["index"])
            else:
                index = count_by_lang[lang] if use_index else None

            if "delete" in item:
                delete = bool(item["delete"])
            else:
                delete = False

            t = TranslationUpdate(
                language=lang,
                translation=translation,
                index=index,
                delete=delete
            )

            translations.append(t)
            if use_index and "index" not in item:
                count_by_lang[lang] += 1

        return translations

class NationRead(NationBase):
    __translation_key__ = "nation"

    id: int
    default_name: str
    code: str

    is_world_federation_member: bool
    is_confederation_member: bool

    # foreign_keys
    continent_id: Optional[PositiveInt] = None
    region_id: Optional[PositiveInt] = None
    parent_id: Optional[PositiveInt] = None

    # translated
    name: Optional[str] = None
    denonyms: list[str] = Field(default_factory=list)
    name_translations: dict[str, str] = Field(default_factory=dict)
    denonyms_translations: dict[str, list] = Field(default_factory=dict)

    # Geonames attrs
    geonames_id: Optional[PositiveInt] = None

    # Active attrs
    active: bool  

    # timestamp attrs
    created_at: datetime
    updated_at: datetime

    # relationships
    continent: Optional["ContinentRead"] = None
    region: Optional["RegionRead"] = None
    parent: Optional["NationRead"] = None   
    children: list["NationRead"] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }   

    @model_validator(mode="after")
    def fill_name_from_default(self):
        if not self.name:
            self.name = self.default_name
        return self
    
   
    @classmethod
    def from_entity(cls, entity: "NationEntity", *, include_continent: bool = True, include_region: bool = True, include_parent: bool = True, include_children: bool = False) -> "NationRead":
        if not entity.id:
            raise ValueError("Cannot generate read model of an instance without id")
               
        continent = ContinentRead.from_entity(entity.continent) if include_continent and entity.continent else None
        region = RegionRead.from_entity(entity.region) if include_region and entity.region else None
        parent = NationRead.from_entity(entity.parent, include_children=False) if include_parent and entity.parent else None
        children = [NationRead.from_entity(nation, include_parent=False, include_children=True) for nation in entity.children] if include_children else []

        return NationRead(
            id=entity.id,
            default_name=entity.name,
            code=entity.code,
            continent_id=entity.continent_id,
            region_id=entity.region_id,
            parent_id=entity.parent_id,
            is_world_federation_member=entity.is_world_federation_member,
            is_confederation_member=entity.is_confederation_member,
            geonames_id=entity.geonames_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            active=entity.active,
            continent=continent,
            region=region,
            parent=parent,
            children=children
        )
