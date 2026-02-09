from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum
from datetime import datetime

from ..base import Base
from ..mixins import ActiveMixin, TimestampMixin

from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .country import Country
    from .city import City

class PersonNationality(Base, TimestampMixin):
    __tablename__ = "person_countryality"
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey("person.id"), primary_key=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("country.id"), primary_key=True)

    intercountryal_apps: Mapped[int] = mapped_column(default=0)
    intercountryal_goals: Mapped[int] = mapped_column(default=0)
    youth_intercountryal_apps: Mapped[int] = mapped_column(default=0)
    youth_intercountryal_goals: Mapped[int] = mapped_column(default=0)

    retired_from_country: Mapped[bool] = mapped_column(default=False)

    country: Mapped["Country"] = relationship("Country")
    
class Person(Base, ActiveMixin, TimestampMixin):
    __tablename__ = 'person'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    full_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    common_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    display_name: Mapped[str] = mapped_column(nullable=False)

    city_of_birth_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_of_birth: Mapped[datetime] = mapped_column()

    countryalities: Mapped[list[PersonNationality]] = relationship(
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

    def _elegible_countries(self, youth_level: bool = False) -> list["Country"]:
        """
        Returns the list of countries the player can currently be selected for.
        Rules:
        1. If the player has played for any official country, only include that country (unless retired).
        2. If the player hasn't played for any official country, include all official countries they are eligible for.
        3. Always include non-official countries (e.g., Catalonia) if the player has a connection.
        """
        countryality_apps_attr = "youth_intercountryal_apps" if youth_level else "intercountryal_apps"

        countries_played_for = [
            n.country
            for n in self.countryalities
            if n.country.is_confederation_member
            and getattr(n, countryality_apps_attr) > 0
            and not n.retired_from_country
        ]

        if countries_played_for:
            countries = countries_played_for
        else:
            countries = [
                n.country
                for n in self.countryalities
                if n.country.is_confederation_member and not n.retired_from_country
            ]

        # Always add non-official countries
        countries.extend([
            n.country
            for n in self.countryalities
            if not n.country.is_confederation_member and not n.retired_from_country
        ])

        # Remove duplicates and sort by id (stable deterministic result)
        return sorted(
            {country.id: country for country in countries}.values(),
            key=lambda x: x.id
        )
        
    @property
    def elegible_countries(self) -> list["Country"]:
        return self._elegible_countries()
    
    @property
    def elegible_countries_at_youth_level(self) -> list["Country"]:
        return self._elegible_countries(youth_level=True)

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
    