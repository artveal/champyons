from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship     

from champyons.core.config import config
from ..base import Base
from ..mixins import ActiveMixin, TimestampMixin

from datetime import datetime
from enum import Enum
    
class UserRoleEnum(str, Enum):
    ADMIN = "admin"

class UserRole(Base):
    __tablename__ = "user_role"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), primary_key=True)
    role: Mapped[UserRoleEnum] = mapped_column(
        SQLEnum(UserRoleEnum, native_enum=False), 
        primary_key=True
    )

class User(Base, TimestampMixin, ActiveMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, nullable=True, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)

    # login
    last_login_at: Mapped[datetime|None] = mapped_column(DateTime, nullable=True)

    # user preferences
    language: Mapped[str] = mapped_column(String, default=config.default_lang)
    locale: Mapped[str] = mapped_column(String, default=config.default_locale)
    timezone: Mapped[str] = mapped_column(String, default=config.server_timezone)

    roles: Mapped[list[UserRole]] = relationship(
        "UserRole",
        collection_class=list,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    # helpers
    def has_role(self, role: str | UserRoleEnum) -> bool:
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        return any(r.role == role_enum for r in self.roles)

    def add_role(self, role: str | UserRoleEnum):
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        if not self.has_role(role_enum):
            self.roles.append(UserRole(role=role_enum))

    def remove_role(self, role: str | UserRoleEnum):
        role_enum = role if isinstance(role, UserRoleEnum) else UserRoleEnum(role)
        self.roles = [r for r in self.roles if r.role != role_enum]

    @property
    def is_admin(self) -> bool:
        return self.has_role(UserRoleEnum.ADMIN)


