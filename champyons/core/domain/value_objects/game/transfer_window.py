from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, UTC

@dataclass(frozen=True)
class TransferWindow:
    """
    A window between two dates when transfers are allowed. Dates are always considered from/to 00:00

    When offset is set, you can fix the exact time of the day that the market opens and closes.

    All datetimes are returned with UTC timezone
    """
    start_date: date
    end_date: date

    time_offset: int|float = 0

    def __post_init__(self):
        if self.end_date <= self.start_date:
            raise ValueError(f"End date ({self.end_date}) must be later from start date ({self.start_date})")
        
        if not(-14 <= self.time_offset <= 14):
            raise ValueError(f"Time offset must be between -14 and +14. Provided value: {self.time_offset}")

    @property
    def duration(self) -> int:
        return (self.end_date - self.start_date).days
    
    @property
    def start_datetime(self) -> datetime:
        return self._date_to_datetime(self.start_date, self.time_offset)
    
    @property
    def end_datetime(self) -> datetime:
        return self._date_to_datetime(self.end_date, self.time_offset)
    
    @classmethod
    def default(cls):
        return TransferWindow(
            start_date=date(1970, 1, 1),
            end_date=date(1970, 2, 1)
        )
    
    @staticmethod
    def _date_to_datetime(date: date, time_offset: float = 0) -> datetime:
        return datetime.combine(date, datetime.min.time(), tzinfo=UTC) - timedelta(hours=time_offset)
    
    def check_transfer_market_open(self, datetime: datetime) -> bool:
        " Returns True if this window is opened for given datetime or False, otherwise"
        return self.start_datetime < datetime < self.end_datetime
