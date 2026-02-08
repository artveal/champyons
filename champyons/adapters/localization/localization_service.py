from champyons.core.ports.services.localization_service import LocalizationService
from champyons.core.domain.value_objects.localization import LocalizationContext, LazyString

from fluent.runtime.types import FluentNumber

import datetime
from pathlib import Path

from typing import Optional
from babel import numbers, dates

from .cache import FluentCache

class FluentBabelLocalizationService(LocalizationService):
    def __init__(self, locales_dir: str):
        self.locales_dir = Path(locales_dir)
        self.fluent_cache = FluentCache(
            Path(locales_dir) / "fluent",
            files=["messages.ftl"]
        )

        # defaults:
        self.default_date_fmt = "medium"
        self.default_dt_fmt = "medium"
        self.default_pct_fmt = None
        self.default_currency_fmt = None

    def translate(self, key: str, ctx: LocalizationContext, **params) -> str:
        fluent = self.fluent_cache.get(ctx.language)
        # expand objects
        flattened = self._flatten_kwargs(**params)
        return fluent.format_value(key, **flattened)

    def _flatten_kwargs(self, result: Optional[dict] = None, prefix: Optional[str] = None, **kwargs) -> dict:
        result = result or {}
        for key, value in kwargs.items():
            if value is None:
                continue

            flattened_key = f"{prefix}_{key}" if prefix else key

            # numbers
            if isinstance(value, (int, float)):
                result[flattened_key] = FluentNumber(value)
            # simple values
            elif isinstance(value, (str, bool)):
                result[flattened_key] = value
            # objects: recursively flatten
            elif isinstance(value, "__dict__"):
                for attr in dir(value):
                    if attr.startswith("_") or callable(getattr(value, attr, None)):
                        continue
                    try:
                        attr_value = getattr(value, attr)
                        result = self._flatten_kwargs(result, flattened_key, kwargs={attr: attr_value})
                    except:
                        pass
            else:
                result[flattened_key] = value

        return result
            
    def format_number(self, value: int|float, ctx: LocalizationContext, decimal_places: Optional[int] = None, use_group_separator: bool = True, *, fmt: Optional[str] = None):
        if decimal_places is None:
            decimal_places = 0 if isinstance(value, int) else 2
        # TO-DO: decimal places does not work properly
        return numbers.format_decimal(value, format=fmt, locale=ctx.locale, group_separator=use_group_separator)
    
    def format_date(self, date: datetime.date, ctx: LocalizationContext, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_date_fmt
        return dates.format_date(date, format=fmt, locale=ctx.locale)
    
    def format_datetime(self, dt: datetime.datetime, ctx: LocalizationContext, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_dt_fmt
        return dates.format_datetime(dt, format=fmt, tzinfo=ctx.timezone, locale=ctx.locale)
    
    def format_percentage(self, value: int|float, ctx: LocalizationContext, decimal_places: int = 2, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_pct_fmt
        # TO-DO: review how to manage decimal places
        return numbers.format_percent(value, format=fmt, locale=ctx.locale)
    
    def format_currency(self, value: int, ctx: LocalizationContext, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_currency_fmt
        # TO-DO: decimal places does not work properly
        return numbers.format_currency(value, self.currency, format=fmt, locale=ctx.locale, currency_digits=False)
    
    def format_compact_currency(self, value: int, ctx: LocalizationContext, decimal_places: int = 0, *, fmt: Optional[str] = None) -> str:
        fmt = fmt or self.default_currency_fmt
        return numbers.format_compact_currency(value, self.currency, format_type=fmt, locale=ctx.locale, fraction_digits=decimal_places)
    
    def to_local_time(self, dt: datetime.datetime, ctx: LocalizationContext) -> datetime.datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.UTC)
        return dt.astimezone(ctx.timezone)

    def to_utc_time(self, local_datetime: datetime.datetime, ctx: LocalizationContext) -> datetime.datetime:
        if local_datetime.tzinfo is None:
            local_datetime = local_datetime.replace(tzinfo=ctx.timezone)
        return local_datetime.astimezone(datetime.UTC)
    