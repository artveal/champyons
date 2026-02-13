from dataclasses import dataclass, field
from datetime import date, timedelta

from champyons.core.domain.entities.mixins.timestamp import TimestampMixin
from champyons.core.domain.entities.game.season import Season

import warnings
from typing import Optional

@dataclass
class GameState(TimestampMixin):
    """
    Represents the global state of a game instance.

    Domain rules:
    - There is only ONE active GameState per save file or running server
    - Tracks in-game date, season and simulation progress
    - Controls simulation speed and pausing

    This is a singleton-like entity in the domain
    """

    id: Optional[int] = None

    sim_date: date = field(default_factory=date.today)
    start_sim_date: date = field(default_factory=date.today)

    # current season
    current_season_id: Optional[int] = None
    current_season: Optional[Season] = None

    # simulation control
    is_simulation_running: bool = False

    @property
    def in_game_days_passed(self):
        return (self.sim_date - self.start_sim_date).days
    
    def advance_delta(self, *, years: int = 0, months: int = 0, weeks: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, milliseconds: int = 0) -> None:
        dt = timedelta(
            days=365*years+30*months+days,
            seconds=seconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks
        )
        if self.is_simulation_running:
            self.sim_date += dt
        else:
            warnings.warn("Game is currently paused")

    def advance_to_date(self, new_game_date: date) -> None:
        if self.is_simulation_running:
            self.sim_date = new_game_date
        else:
            warnings.warn("Game is currently paused")

    def pause(self) -> None:
        self.is_simulation_running = False

    def start(self) -> None:
        self.is_simulation_running = True


