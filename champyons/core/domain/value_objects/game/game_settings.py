from dataclasses import dataclass
from datetime import timedelta

@dataclass(frozen=True)
class GameSettings:
    """
    An object repreenting all game settings
    """
    # simulation
    simulation_speed: float = 1.0 # represents how many times per real-life day will pass an in-game day. 3 means that each 8 hours real life, in-game date will be increased by one day.
    injuries_enabled: bool = True

    @property
    def simulation_interval(self) -> timedelta:
        """ Returns the timedelta that must pass before advancing ONE in-game time"""
        return timedelta(days=1) / self.simulation_speed

    @classmethod
    def default(cls):
        return cls()