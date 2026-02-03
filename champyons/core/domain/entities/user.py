from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from ..enums.user import UserRoleEnum

from .mixins.active import ActiveMixin
from .mixins.timestamp import TimestampMixin

@dataclass
class UserRole:
    """Rol asociado a un usuario."""
    role: UserRoleEnum

@dataclass
class User(TimestampMixin, ActiveMixin):
    """Modelo de dominio de un usuario."""
    id: Optional[int] = None
    username: str = ""
    email: Optional[str] = None
    password_hash: Optional[str] = None

    # login
    last_login_at: Optional[datetime] = None

    # preferencias
    language: str = "es"
    locale: str = "es_ES"
    timezone: str = "Europe/Madrid"

    # roles
    roles: List[UserRole] = field(default_factory=list)

    # helpers
    def has_role(self, role: str | UserRoleEnum) -> bool:
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        return any(r.role == role_enum for r in self.roles)

    def add_role(self, role: str | UserRoleEnum):
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        if not self.has_role(role_enum):
            self.roles.append(UserRole(role_enum))

    def remove_role(self, role: str | UserRoleEnum):
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        self.roles = [r for r in self.roles if r.role != role_enum]

    @property
    def is_admin(self) -> bool:
        return self.has_role(UserRoleEnum.ADMIN)