"""
API utilities for timezone management.

This module works together with core.timezone.context.
Provides:
- Converting datetime objects between UTC and user timezone
- Utilities: current UTC/local time, validation, listing timezones
"""

from datetime import datetime, UTC
from zoneinfo import ZoneInfo, available_timezones
from .context import get_timezone
from champyons.core.config import config

def server_tzinfo() -> ZoneInfo:
    return UTC

def server_to_local(dt_utc: datetime) -> datetime:
    """
    Convert a aware datetime from server timezone to the user's current timezone.
    Raises ValueError if dt_utc is naive.
    """
    if dt_utc.tzinfo is None:
        raise ValueError("dt_utc must be timezone-aware (UTC)")
    return dt_utc.astimezone(get_timezone())

def local_to_server(dt_local: datetime) -> datetime:
    """
    Convert a local-aware datetime to server timezone.
    If dt_local is naive, assume it is in the current user timezone.
    """
    if dt_local.tzinfo is None:
        dt_local = dt_local.replace(tzinfo=get_timezone())
    return dt_local.astimezone(server_tzinfo())

# ----------------------------------------------------------------------
# Current timestamps
# ----------------------------------------------------------------------
def now_server() -> datetime:
    """Return current server datetime (timezone-aware)."""
    return datetime.now(tz=server_tzinfo())

def now_local() -> datetime:
    """Return current datetime in user timezone (timezone-aware)."""
    return now_server().astimezone(get_timezone())

# ----------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------
def list_timezones() -> list[str]:
    """Return a sorted list of all valid IANA timezone names."""
    return sorted(available_timezones())

