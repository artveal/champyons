from collections import defaultdict
from typing import Iterable, List
import sqlalchemy as sa
from sqlalchemy.orm import Session
from champyons.adapters.persistence.sqlalchemy.models.translation import Translation as TranslationModel
from champyons.core.ports.repositories.translations import TranslationRepository, TranslatedFields, TranslationKey

class SqlAlchemyTranslationRepository(TranslationRepository):
    """SQLAlchemy implementation of TranslationRepository."""
    def __init__(self, session: Session):
        self.session = session

    def get_translations(self, *, keys: Iterable[tuple[str, int]], lang: str|None = None) -> dict[TranslationKey, TranslatedFields]:
        ''' Returns a dictionary of translations with (entity, foreign_key) as key and a dict of translatable fields for given language or all languages if lang is not given'''
        keys = list(keys)
        if not keys:
            return dict()
        
        stmt = sa.select(
                TranslationModel.entity,
                TranslationModel.foreign_key,
                TranslationModel.field,
                TranslationModel.index,
                TranslationModel.language,
                TranslationModel.translation
            )
        
        if lang:
            stmt = stmt.where(TranslationModel.language == lang[:2])
        
        stmt = (
            stmt
            .where(sa.tuple_(TranslationModel.entity, TranslationModel.foreign_key).in_(keys))
            .order_by(TranslationModel.field, TranslationModel.index)
        )
        result = self.session.execute(stmt).all()

        translations: dict[TranslationKey, TranslatedFields] = defaultdict(lambda: defaultdict(dict))

        for entity, foreign_key, field, index, language, value in result:
            key = (entity, foreign_key)

            field_translations = translations[key][field]
            
            if language not in field_translations:
                field_translations[language] = value
                continue

            existing = field_translations[language]

            if isinstance(existing, list):
                existing.append(value)
            else:
                field_translations[language] = [existing, value]

        return translations
    
    def _get_by_keys(self, entity: str, foreign_key: int, field: str, language: str, index: int|None = None) -> TranslationModel|None:
        stmt = sa.select(TranslationModel).where(
            TranslationModel.entity == entity,
            TranslationModel.foreign_key == foreign_key,
            TranslationModel.field == field,
            TranslationModel.language == language,
            TranslationModel.index == index
        )
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def save(self, entity: str, foreign_key: int, field: str, language: str, translation: str, index: int|None = None) -> None:
        language = language[:2]
        translation_instance = self._get_by_keys(entity, foreign_key, field, language, index)
        if translation_instance:
            translation_instance.translation = translation
        else:
            translation_instance = TranslationModel(
                entity=entity,
                foreign_key=foreign_key,
                field=field,
                language=language,
                translation=translation,
                index=index
            )
            self.session.add(translation_instance)

        self.session.commit()
        self.session.refresh(translation_instance)

    def delete(self, entity: str, foreign_key: int, field: str, language: str, index: int|None = None) -> None:
        translation_instance = self._get_by_keys(entity, foreign_key, field, language[:2], index)
        if translation_instance:
            self.session.delete(translation_instance)
            self.session.commit()