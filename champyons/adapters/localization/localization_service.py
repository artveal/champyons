from champyons.core.ports.services.localization_service import LocalizationService
from champyons.core.domain.value_objects.localization import LocalizationContext

import datetime

from typing import Optional
from babel import numbers, dates
from zoneinfo import ZoneInfo

class BabelGettextI18NService(LocalizationService):
    def __init__(self, language: str, locale: str, timezone: str|ZoneInfo, currency: str):
        self.localization_ctx = LocalizationContext(
            language=language,
            locale=locale,
            timezone=ZoneInfo(timezone) if isinstance(timezone, str) else timezone
        )

        self.currency = currency

        # defaults:
        self.default_date_fmt = "medium"
        self.default_dt_fmt = "medium"
        self.default_pct_fmt = None
        self.default_currency_fmt = None

    def translate(self, key: str, **params) -> str:
        # TO-DO. Now is a placeholder. We will be using Fluent.runtime
        return f"[{self.localization_ctx.language}] {key}"
    
    def format_number(self, value: int|float, decimal_places: Optional[int] = None, use_group_separator: bool = True, *, fmt: Optional[str] = None):
        if decimal_places is None:
            decimal_places = 0 if isinstance(value, int) else 2
        # TO-DO: decimal places does not work properly
        return numbers.format_decimal(value, format=fmt, locale=self.localization_ctx.locale, group_separator=use_group_separator)
    
    def format_date(self, date: datetime.date, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_date_fmt
        return dates.format_date(date, format=fmt, locale=self.localization_ctx.locale)
    
    def format_datetime(self, dt: datetime.datetime, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_dt_fmt
        return dates.format_datetime(dt, format=fmt, tzinfo=self.localization_ctx.timezone, locale=self.localization_ctx.locale)
    
    def format_percentage(self, value: int|float, decimal_places: int = 2, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_pct_fmt
        # TO-DO: review how to manage decimal places
        return numbers.format_percent(value, format=fmt, locale=self.localization_ctx.locale)
    
    def format_currency(self, value: int, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_currency_fmt
        # TO-DO: decimal places does not work properly
        return numbers.format_currency(value, self.currency, format=fmt, locale=self.localization_ctx.locale, currency_digits=False)
    
    def format_compact_currency(self, value: int, decimal_places: int = 0, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_currency_fmt
        return numbers.format_compact_currency(value, self.currency, format_type=fmt, locale=self.localization_ctx.locale, fraction_digits=decimal_places)
    
    def to_local_time(self, dt: datetime.datetime) -> datetime.datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.UTC)
        return dt.astimezone(self.localization_ctx.timezone)

    def to_utc_time(self, local_datetime: datetime.datetime) -> datetime.datetime:
        if local_datetime.tzinfo is None:
            local_datetime = local_datetime.replace(tzinfo=self.localization_ctx.timezone)
        return local_datetime.astimezone(datetime.UTC)
    