from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from champyons.core.domain.enums.user import UserRoleEnum


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    language: Optional[str] = None
    locale: Optional[str] = None
    timezone: Optional[str] = None

class UserRoleSchema(BaseModel):
    role: UserRoleEnum

    class Config:
        use_enum_values = True

class UserCreate(UserBase):
    password: str

# ---- Update ----
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None
    timezone: Optional[str] = None
    roles: Optional[List[UserRoleEnum]] = None  # optional to modify roles

# ---- Read / Response ----
class UserRead(UserBase):
    id: int
    roles: List[UserRoleSchema] = []
    last_login_at: Optional[datetime] = None
    is_admin: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    active: bool = True

    class Config:
        orm_mode = True
        use_enum_values = True
