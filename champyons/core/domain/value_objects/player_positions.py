from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set
from champyons.core.domain.enums.player_positions import Position


@dataclass
class BasePositionList:
    positions: List[Position] = field(default_factory=list)
    def __post_init__(self):
        self._remove_duplicates()

    def _remove_duplicates(self):
        seen: Set[Position] = set()
        unique_positions: List[Position] = []
        for pos in self.positions:
            if pos not in seen:
                unique_positions.append(pos)
                seen.add(pos)
        self.positions = unique_positions


@dataclass
class PitchPositionList(BasePositionList):
    pass


@dataclass
class PlayerPositionList(BasePositionList):
    def __post_init__(self):
        super().__post_init__()
        self._exclude_center_sides()

    def _exclude_center_sides(self):
        self.positions = [pos for pos in self.positions if abs(pos.side) != 1]