from pydantic import BaseModel, PositiveInt, Field, model_validator
from datetime import datetime
from collections import defaultdict

from typing import Optional, TypeVar, Union, Any, TYPE_CHECKING

from .translation import TranslationBase, TranslationCreate, TranslationUpdate

TTranslation = TypeVar("TTranslation", bound=TranslationBase)
TranslationInput = Union[TTranslation, dict[str, str]]

if TYPE_CHECKING:
    from champyons.schemas.nation import NationRead
    from champyons.core.domain.entities.geography.region import Region as RegionEntity

class RegionBase(BaseModel):
    default_name: str

    # Geonames attrs
    geonames_id: Optional[PositiveInt] = None

    # Active attrs
    active: bool

class RegionUpsert(BaseModel):
    translated_names: list[TranslationInput] = Field(default_factory=list, init_var=True)

    @model_validator(mode="before")
    def convert_translations(cls, values: dict[str, Any]) -> dict[str, Any]:
        raw_name_translations: list[TranslationInput] = values.get("translated_names", [])          
        values["name_translations"] = cls._parse_translations(raw_name_translations, use_index=False)
        return values
    
    @staticmethod
    def _parse_translations(raw_translations: list[TranslationInput], use_index: bool = False):
        pass

class RegionCreate(RegionUpsert, RegionBase):
     # translations
    name_translations: list[TranslationCreate] = Field(default_factory=list, init=False)

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

class RegionUpdate(RegionUpsert, RegionBase):
    default_name: Optional[str] = None

    # translations
    name_translations: list[TranslationUpdate] = Field(default_factory=list, init=False)

    # Active attrs
    active: Optional[bool] = True

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

class RegionRead(RegionBase):
    __translation_key__ = "region"

    id: int
    default_name: str

    # Geonames attrs
    geonames_id: Optional[PositiveInt] = None

    # Active attrs
    active: bool

    # translated 
    name: Optional[str] = None
    name_translations: dict[str, str] = Field(default_factory=dict)

    # timestamp attrs
    created_at: datetime
    updated_at: datetime

    # relationships
    nations: list["NationRead"] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    } 

    @model_validator(mode="after")
    def fill_name_from_default(self):
        if not self.name:
            self.name = self.default_name
        return self

    @classmethod
    def from_entity(cls, entity: "RegionEntity", *, include_nations: bool = False) -> "RegionRead":
        if not entity.id:
            raise ValueError("Cannot generate read model of an instance without id")
               
        if include_nations:
            from champyons.schemas.nation import NationRead

            nations = [
                NationRead.from_entity(nation)
                for nation in entity.nations
            ]
        else:
            nations = []
     
        return RegionRead(
            id=entity.id,
            default_name=entity.name,
            geonames_id=entity.geonames_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            active=entity.active,
            nations=nations,
        )

