from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..types import JSONEncodedDict, JSONEncodedList

from .person import Profile


class PlayerProfile(Profile):
    __tablename__ = 'player_profile'

    skills: Mapped[dict[str, float]] = mapped_column(JSONEncodedDict, nullable=False, default=dict)
    positions: Mapped[list[str]] = mapped_column(JSONEncodedList, nullable=False, default=list)

    __mapper_args__ = {
        "polymorphic_identity": "player",
        "concrete": True
    }