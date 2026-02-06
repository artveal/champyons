from dataclasses import dataclass
from zoneinfo import ZoneInfo

@dataclass(frozen=True)
class LocalizationContext:
    language: str
    locale: str
    timezone: ZoneInfo