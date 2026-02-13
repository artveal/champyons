from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, TYPE_CHECKING
from champyons.core.domain.entities.mixins import ActiveMixin, TimestampMixin
from champyons.core.domain.value_objects.game.transfer_window import TransferWindow
from champyons.core.domain.value_objects.game.game_settings import GameSettings

if TYPE_CHECKING:
    from champyons.core.domain.entities.competitions.competition_edition import CompetitionEdition

@dataclass
class Season(ActiveMixin, TimestampMixin):
    """
    Represents a football season, a cyclic period of time where competitions are played, transfer windows are opened/closed, etc.

    Domain Rules:
    - Only ONE season can be active at a time.
    - Seasons are indexed and follow a progression (1, 2, 3...)
    - season name format can be managed via season_name_fmt
    - Dates/times are always stores in real-life datetime. Methods for calculation of in-game dates are provided
    - Each season has a in_game_end_date. Start date is always the previous season's end date (for the first season it will be starting simulation date)
    - transfer windows can be overriden for each nationality by NationRules.
    """

    id: Optional[int] = None
    start_date: date = date.min 
    end_date: date = date.max
    name_fmt: str = "{index} ({start:%YYYY}-{end:%YY})"

    index: int = 1

    # Competition editions played this season
    competition_editions_ids: list[int] = field(default_factory=list)
    competition_editions: list[CompetitionEdition] = field(default_factory=list)

    default_transfer_window_1: TransferWindow|None = None
    default_transfer_window_2: TransferWindow|None = None

    settings: GameSettings = field(default_factory=GameSettings.default)

    @property
    def name(self) -> str:
        ctx = {
            "index": self.index,
            "start": self.start_date,
            "end": self.end_date
        }
        return self.name_fmt.format(**ctx)
    
    @property
    def duration(self) -> int:
        return (self.end_date - self.start_date).days
    
    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError(f"Season index must be and integer grater than 0.")
        
        if self.end_date <= self.start_date:
            raise ValueError(f"End date ({self.end_date}) must be later from start date ({self.start_date})")
    
    def check_default_market_open(self, datetime: datetime) -> bool:
        w1_opened = self.default_transfer_window_1 and self.default_transfer_window_1.check_transfer_market_open(datetime)
        w2_opened = self.default_transfer_window_2 and self.default_transfer_window_2.check_transfer_market_open(datetime)
        return w1_opened or w2_opened
    
    @classmethod
    def create_next_season(cls, previous_season: "Season"):
        " Generates a new season with the same duration and transfer windows duration from previous season"
        default_tws = dict()
        for index, tw in enumerate((previous_season.default_transfer_window_1, previous_season.default_transfer_window_2)):
            if not tw:
                continue
            default_tws[index] = TransferWindow(
                start_date=tw.start_date + previous_season.duration,
                end_date=tw.end_date + previous_season.duration,
                time_offset=tw.time_offset
            )
        return cls(
            start_date = previous_season.start_date + previous_season.duration,
            end_date = previous_season.end_date + previous_season.duration,
            index = previous_season.index + 1,
            default_transfer_window_1 = default_tws.get(0),
            default_transfer_window_2 = default_tws.get(1)
        )

