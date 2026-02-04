from abc import ABC, abstractmethod
from typing import Iterable, Union, Any

TranslationKey = tuple[str, int]
TranslatedValue = Union[str, list[str]]
TranslatedFields = dict[str, dict[str, TranslatedValue]]

class TranslationRepository(ABC):
    @abstractmethod
    def get_translations(self, *, keys: Iterable[TranslationKey], lang: str|None = None) -> dict[TranslationKey, TranslatedFields]:
        pass

    @abstractmethod
    def save(self, entity: str, foreign_key: int, field: str, language: str, translation: str, index: int|None = None) -> None:
        pass

    @abstractmethod
    def delete(self, entity: str, foreign_key: int, field: str, language: str, index: int|None = None) -> None:
        pass