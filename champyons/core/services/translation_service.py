from champyons.core.repositories.translations import TranslationRepository, TranslatedFields, TranslationKey
from champyons.core.i18n.context import get_lang
from typing import Any, Optional, Sequence, TypeVar
from collections import defaultdict
from champyons.schemas.translation import TranslationCreate, TranslationRead

from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)
type TranslationList = Sequence[TranslationCreate]|Sequence[TranslationRead]

class ReadModelTranslationService:
    def __init__(self, translation_repo: TranslationRepository) -> None:
        self._repo = translation_repo

    def translate(self, model: TModel, lang: str|None = None) -> TModel:
        lang = lang or get_lang()

        keys = self._collect_translation_keys(model)
        if not keys:
            return model
        
        translations = self._repo.get_translations(keys=keys)

        self._apply_translations(model, translations, lang[:2])
        return model
    
    def get_translations_of_model(self, model: BaseModel, lang: str|None = None) -> TranslatedFields:
        lang = lang or get_lang()
        entity: str|None = getattr(model, "__translation_key__", None)
        if entity is None:
            raise ValueError(f"Cannot translate {model.__class__.__name__} because has no '__translation_key__' attribute")
        
        foreign_key: int|None = getattr(model, "id", None)
        if foreign_key is None:
            raise ValueError(f"Cannot translate {model.__class__.__name__} because has no 'id' attribute")
        
        key: TranslationKey = (entity, foreign_key)
        return self._repo.get_translations(keys=[key], lang=lang).get(key, {})
    
    def _collect_translation_keys(self, obj: Any, collected: set[TranslationKey] | None = None) -> set[TranslationKey]:
        collected = collected or set()

        if isinstance(obj, BaseModel):
            key = self._get_translation_key(obj)
            if key is not None:
                collected.add(key)

            for value in obj.__dict__.values():
                self._collect_translation_keys(value, collected)
            
        elif isinstance(obj, list):
            for item in obj:
                self._collect_translation_keys(item, collected)

        return collected
    
    def _apply_translations(self, obj: Any, translations: dict[TranslationKey, TranslatedFields], lang: str) -> None:
        if isinstance(obj, BaseModel):
            key = self._get_translation_key(obj)
            if key is not None and key in translations:
                self._apply_translation_to_model(obj, translations[key], lang=lang)

            for field_name, value in obj.__dict__.items():
                self._apply_translations(value, translations, lang)

        elif isinstance(obj, list):
            for item in obj:
                self._apply_translations(item, translations, lang)

    def _apply_translation_to_model(self, model: BaseModel, fields: TranslatedFields, lang: str) -> None:
        for field_name, translations in fields.items():
            for _lang, translation in translations.items():
                if not hasattr(model, field_name) or lang != _lang:
                    continue
                setattr(model, field_name, translation)

            translations_dict_field_name = f"{field_name}_translations"
            if not hasattr(model, translations_dict_field_name):
                continue
            setattr(model, translations_dict_field_name, translations)
            

    def _get_translation_key(self, model: BaseModel) -> TranslationKey | None:
        entity_id = getattr(model, "id", None)
        if entity_id is None or entity_id < 0:
            return None
        
        entity = getattr(model, "__translation_key__", None)
        if entity is None:
            return None
        
        return (entity, entity_id)
    
class TranslationService:
    def __init__(self, translation_repo: TranslationRepository) -> None:
        self._repo = translation_repo

    def set_translations(self, *, entity: str, foreign_key: int, field_name: str, translations: TranslationList, use_index: bool = False) -> None:
        """
        Create or update multiple translations for given entity and field. If use_index is True, automatic index will be assigned for each item, otherwise, one translation (the first) for each leanguge will be saved wihtout index
        """
        # manage deletions
        to_delete = [t for t in translations if getattr(t, "delete", False) is True]
        for t in to_delete:
            self.delete_translation(
                entity=entity,
                foreign_key=foreign_key,
                field=field_name,
                language=t.language,
                index=getattr(t, "index", None)
            )

        # filter translations to save
        translations_to_save = [t for t in translations if not getattr(t, "delete", False)]

        # group translations by language
        translations_by_language: dict[str, list[str]] = defaultdict(list)
        for t in translations_to_save:
            translations_by_language[t.language].append(t.translation)

        for language, translations_list in translations_by_language.items():
            if use_index is False and len(translations_list) == 1:
                translation = translations_list[0]
                self._repo.save(
                    entity=entity,
                    foreign_key=foreign_key,
                    field=field_name,
                    translation=translation,
                    language=language,
                )
                continue
            
            for index, translation in enumerate(translations_list):
                self._repo.save(
                    entity=entity,
                    foreign_key=foreign_key,
                    field=field_name,
                    translation=translation,
                    language=language,
                    index=index
                )               

    def delete_translation(
        self,
        *,
        entity: str,
        foreign_key: int,
        field: str,
        language: Optional[str] = None,
        index: Optional[int] = None
    ) -> None:
        """
        Delete a translation for a single field. If language is None, deletes
        the translation for the default language.
        """
        language = language or get_lang()
        self._repo.delete(
            entity=entity,
            foreign_key=foreign_key,
            field=field,
            language=language,
            index=index
        )