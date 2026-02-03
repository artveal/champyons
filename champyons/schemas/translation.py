from typing import Optional
from pydantic import BaseModel, PositiveInt

ForeignKey = PositiveInt

class TranslationBase(BaseModel):
    language: str
    translation: str
    index: Optional[int] = None
   
class TranslationCreate(TranslationBase):
    pass

class TranslationUpdate(TranslationBase):
    translation: Optional[str]
    delete: bool = False

class TranslationRead(TranslationBase):
    id: PositiveInt
    entity: str
    field: str
    foreign_key: ForeignKey