from dataclasses import dataclass
from zoneinfo import ZoneInfo
from typing import Callable

@dataclass(frozen=True)
class LocalizationContext:
    language: str
    locale: str
    timezone: ZoneInfo

    @classmethod
    def default(cls) -> "LocalizationContext":
        return cls(
            language="en",
            locale="en_US",
            timezone=ZoneInfo("UTC")
        )
    
class LazyString:
    """A string-like object that evaluates the translation only when needed."""
    def __init__(self, func: Callable[[], str]):
        self._func = func

    def __str__(self):
        return self._func()

    def __repr__(self):
        return f"LazyString({str(self)})"

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def __mod__(self, other):
        return str(self) % other

    def format(self, *args, **kwargs):
        return str(self).format(*args, **kwargs)