from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from ..enums.user import UserRoleEnum

from .mixins.active import ActiveMixin
from .mixins.timestamp import TimestampMixin

@dataclass
class User(TimestampMixin, ActiveMixin):
    """ A user represents a software player.
    - If the game is somehow adapted for a multiplayer game, each user will be an internet user.
    - If adapted to be a desktop single player game, there will be only a user

    Each user can be represented by a person (Person entity) in the simulation world. People are 
    considered in-game entities that exist only in the simulation.
    """
    id: Optional[int] = None
    username: str = ""
    email: Optional[str] = None
    password_hash: Optional[str] = None

    # login
    last_login_at: Optional[datetime] = None

    # user preferences
    language: str = "es"
    locale: str = "es_ES"
    timezone: str = "Europe/Madrid"

    # roles
    roles: List[UserRoleEnum] = field(default_factory=list)

    # person profile. to be implemented
    #person: Optional["Person"] = None

    def __post_init__(self) -> None:
        # Validate username
        if not self.username or not self.username.strip():
            raise ValueError("Username cannot be empty")
        
        # Validate password (if provided)
        if self.password_hash is not None:
            if not self.password_hash.strip():
                raise ValueError("Password hash cannot be empty string")
            # Opcional: verificar que parece un hash válido (ej: bcrypt empieza con $2b$)
            if not self.password_hash.startswith("$2"):
                raise ValueError("Password hash format appears invalid")
            
        # Validate email (if provided) and its format
        if self.email is not None:
            if not self.email.strip():
                raise ValueError("Email cannot be empty string")
            # Validación básica de formato email
            if "@" not in self.email or "." not in self.email.split("@")[-1]:
                raise ValueError(f"Invalid email format: '{self.email}'")
        
        # Validate language code (ISO 639-1)
        if len(self.language) != 2:
            raise ValueError(
                f"Invalid language code: '{self.language}'. "
                f"Must be 2 characters (ISO 639-1)"
            )
        
        # Validate locale format (ISO 639-1_ISO 3166-1)
        if "_" not in self.locale or len(self.locale.split("_")) != 2:
            raise ValueError(
                f"Invalid locale format: '{self.locale}'. "
                f"Expected format: 'es_ES', 'en_US', etc."
            )

    # helpers
    def has_role(self, role: str | UserRoleEnum) -> bool:
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        return role_enum in self.roles

    def add_role(self, role: str | UserRoleEnum):
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        if not self.has_role(role_enum):
            self.roles.append(role_enum)

    def remove_role(self, role: str | UserRoleEnum):
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        self.roles = [r for r in self.roles if r != role_enum]

    @property
    def is_admin(self) -> bool:
        return self.has_role(UserRoleEnum.ADMIN)
    
    
