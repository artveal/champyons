from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum
from datetime import datetime

from ..base import Base
from ..mixins import ActiveMixin, TimestampMixin

from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .nation import Nation
    from .city import City

class PersonNationality(Base, TimestampMixin):
    __tablename__ = "person_nationality"
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey("person.id"), primary_key=True)
    nation_id: Mapped[int] = mapped_column(Integer, ForeignKey("nation.id"), primary_key=True)

    international_apps: Mapped[int] = mapped_column(default=0)
    international_goals: Mapped[int] = mapped_column(default=0)
    youth_international_apps: Mapped[int] = mapped_column(default=0)
    youth_international_goals: Mapped[int] = mapped_column(default=0)

    retired_from_nation: Mapped[bool] = mapped_column(default=False)

    nation: Mapped["Nation"] = relationship("Nation")
    
class Person(Base, ActiveMixin, TimestampMixin):
    __tablename__ = 'person'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    full_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    common_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    display_name: Mapped[str] = mapped_column(nullable=False)

    city_of_birth_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_of_birth: Mapped[datetime] = mapped_column()

    nationalities: Mapped[list[PersonNationality]] = relationship(
        "PersonNationality",
        collection_class=list,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    # Relación a perfiles
    profiles: Mapped[list["Profile"]] = relationship(
        "Profile",
        back_populates="person",
        cascade="all, delete-orphan"
    )

    def _elegible_nations(self, youth_level: bool = False) -> list["Nation"]:
        """
        Returns the list of nations the player can currently be selected for.
        Rules:
        1. If the player has played for any official nation, only include that nation (unless retired).
        2. If the player hasn't played for any official nation, include all official nations they are eligible for.
        3. Always include non-official nations (e.g., Catalonia) if the player has a connection.
        """
        nationality_apps_attr = "youth_international_apps" if youth_level else "international_apps"

        nations_played_for = [
            n.nation
            for n in self.nationalities
            if n.nation.is_confederation_member
            and getattr(n, nationality_apps_attr) > 0
            and not n.retired_from_nation
        ]

        if nations_played_for:
            nations = nations_played_for
        else:
            nations = [
                n.nation
                for n in self.nationalities
                if n.nation.is_confederation_member and not n.retired_from_nation
            ]

        # Always add non-official nations
        nations.extend([
            n.nation
            for n in self.nationalities
            if not n.nation.is_confederation_member and not n.retired_from_nation
        ])

        # Remove duplicates and sort by id (stable deterministic result)
        return sorted(
            {nation.id: nation for nation in nations}.values(),
            key=lambda x: x.id
        )
        
    @property
    def elegible_nations(self) -> list["Nation"]:
        return self._elegible_nations()
    
    @property
    def elegible_nations_at_youth_level(self) -> list["Nation"]:
        return self._elegible_nations(youth_level=True)

class Profile(ActiveMixin, TimestampMixin, Base):
    __abstract__ = True  # Abstract

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey('person.id'))
    person: Mapped[Person] = relationship("Person", back_populates="profiles")

class ManagerProfile(Profile):
    __tablename__ = 'manager_profile'

    coaching_skill: Mapped[float] = mapped_column(default=0.0)
    style: Mapped[str] = mapped_column(default="neutral")

    __mapper_args__ = {
        "polymorphic_identity": "coach",
        "concrete": True
    }
    