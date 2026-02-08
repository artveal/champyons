from abc import ABC, abstractmethod
import datetime

from typing import Optional
from champyons.core.domain.value_objects.localization import LocalizationContext

class LocalizationService(ABC):
    @abstractmethod
    def translate(self, key: str, ctx: LocalizationContext, **params) -> str: ...

    @abstractmethod
    def format_number(self, value: int|float, ctx: LocalizationContext, decimal_places: Optional[int], use_group_separator: bool, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_date(self, date: datetime.date, ctx: LocalizationContext, *,  fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_datetime(self, dt: datetime.datetime, ctx: LocalizationContext, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_percentage(self, value: int|float, ctx: LocalizationContext, decimal_places: int, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_currency(self, value: int, currency: str, ctx: LocalizationContext, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def format_compact_currency(self, value: int|float, currency: str, decimal_places: int, ctx: LocalizationContext, *, fmt: Optional[str]) -> str: ...

    @abstractmethod
    def to_local_time(self, dt: datetime.datetime, ctx: LocalizationContext) -> datetime.datetime: ...

    @abstractmethod
    def to_utc_time(self, local_datetime: datetime.datetime, ctx: LocalizationContext) -> datetime.datetime: ...




