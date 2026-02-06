from .context import get_locale
from champyons.core.timezone.context import get_timezone
from babel import dates, numbers

from typing import Literal

import datetime

# format dates
def format_date(date: datetime.date, format: str = 'medium', locale: str|None = None) -> str:
    locale = locale or get_locale()
    return dates.format_date(date, format=format, locale=locale)

# format datetime
def format_datetime(datetime: datetime.datetime, format: str = "medium", timezone: datetime.tzinfo|None = None, locale: str|None = None) -> str: 
    locale = locale or get_locale()
    tzinfo = timezone or get_timezone()
    return dates.format_datetime(
        datetime=datetime,
        format=format,
        tzinfo=tzinfo,
        locale=locale
    )

# format percentage
def format_percentage(number, format: str|numbers.NumberPattern|None, locale: str|None = None, *, decimal_quantization: bool = True, group_separator: bool = True, numbering_system: str|Literal['default'] = 'latn'):
    locale = locale or get_locale()
    return numbers.format_percent(
        number, 
        format=None,
        locale=locale,
        decimal_quantization=decimal_quantization,
        group_separator=group_separator,
        numbering_system=numbering_system
    )

def format_currency(number, currency: str, format, locale):
    locale = locale or get_locale()
    return
'''
    return numbers.format_currency(
        number, currency, 
        format=format,
        locale=locale,
        currency_digits=currency_digits,
        format_type=format_type,
        decimal_quantization=decimal_quantization,
        group_separator=group_separator
        numbering_system=numbering_system
    )
'''
