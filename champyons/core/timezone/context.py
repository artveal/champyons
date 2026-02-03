from champyons.core.config import config

from contextlib import contextmanager
from contextvars import ContextVar

from typing import Generator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

current_tzinfo: ContextVar[ZoneInfo] = ContextVar("current_tzinfo", default=ZoneInfo(config.server_timezone))

def get_timezone() -> ZoneInfo:
    """
    Return the current timezone for this execution context.
    Always returns a ZoneInfo instance.
    """
    try:
        return current_tzinfo.get()
    except LookupError:
        return ZoneInfo(config.server_timezone)

def set_timezone(tzinfo: str|ZoneInfo):
    """
    Set the timezone for this execution context.
    Applications are responsible for detecting the user's timezone
    (e.g., browser, OS, config file, DB).
    """
    if isinstance(tzinfo, str):
        try:
            tzinfo = ZoneInfo(tzinfo)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Invalid timezone: {tzinfo}")
    elif not isinstance(tzinfo, ZoneInfo):
        raise TypeError("tz must be a str or ZoneInfo instance")
    
    current_tzinfo.set(tzinfo)

@contextmanager
def use_timezone(tz_info: str|ZoneInfo) -> Generator[None, None, None]:
    """Temporarily set a timezone for the current context."""
    if not isinstance(tz_info, ZoneInfo):
        tz_info = ZoneInfo(tz_info)
    token = current_tzinfo.set(tz_info)
    try:
        yield
    finally:
        current_tzinfo.reset(token)