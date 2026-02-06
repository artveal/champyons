from pydantic import BaseModel, Field, conint, confloat
from typing import List, Optional, Union, Annotated
from datetime import datetime

# ---- Base / Shared ----
class ProfileBase(BaseModel):
    id: int
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# ---- PlayerProfile ----
class PlayerProfileRead(ProfileBase):
    shooting: float = 0.0
    passing: float = 0.0
    dribbling: float = 0.0
    profile_type: str = Field(default="player", alias="type")

# ---- CoachProfile ----
class CoachProfileRead(ProfileBase):
    coaching_skill: float = 0.0
    style: str = "neutral"
    profile_type: str = Field(default="coach", alias="type")

# ---- Union de perfiles ----
ProfileRead = Union[PlayerProfileRead, CoachProfileRead]

# ---- Persona ----
class PersonBase(BaseModel):
    name: str
    age: int

class PersonRead(PersonBase):
    id: int
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    profiles: List[ProfileRead] = []

    class Config:
        orm_mode = True

# ---- Base Profile ----
class ProfileCreateBase(BaseModel):
    active: Optional[bool] = True

# ---- PlayerProfileCreate ----
class PlayerProfileCreate(ProfileCreateBase):
    shooting: Optional[Annotated[float, confloat(ge=0.0)]] = 0.0
    passing: Optional[Annotated[float, confloat(ge=0.0)]] = 0.0
    dribbling: Optional[Annotated[float, confloat(ge=0.0)]] = 0.0

# ---- CoachProfileCreate ----
class CoachProfileCreate(ProfileCreateBase):
    coaching_skill: Optional[Annotated[float, confloat(ge=0.0)]] = 0.0
    style: Optional[str] = "neutral"

# ---- Union de perfiles para creación ----
ProfileCreate = Union[PlayerProfileCreate, CoachProfileCreate]

# ---- Persona Create ----
class PersonCreate(BaseModel):
    name: str
    age: Annotated[float, confloat(ge=0.0)]
    active: Optional[bool] = True
    profiles: Optional[List[ProfileCreate]] = []

    class Config:
        orm_mode = True
