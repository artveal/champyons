from abc import ABC, abstractmethod
import datetime

from typing import Optional

class LocalizationService(ABC):
    @abstractmethod
    def translate(self, key: str, **params) -> str: ...

    @abstractmethod
    def format_number(self, value: int|float, decimal_places: Optional[int], use_group_separator: bool, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_date(self, date: datetime.date, *,  fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_datetime(self, dt: datetime.datetime, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_percentage(self, value: int|float, decimal_places: int, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_currency(self, value: int, currency: str, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_compact_currency(self, value: int|float, currency: str, decimal_places: int, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def to_local_time(self, dt: datetime.datetime) -> datetime.datetime: ...

    @abstractmethod
    def to_utc_time(self, local_datetime: datetime.datetime) -> datetime.datetime: ...




