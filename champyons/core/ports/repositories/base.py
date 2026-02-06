from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    ''' Abstract base repository with basic CRUD operations'''

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T | None:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        pass