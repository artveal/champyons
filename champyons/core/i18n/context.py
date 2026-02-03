from champyons.core.config import config

from contextlib import contextmanager
from contextvars import ContextVar

from typing import Generator, Optional
from locale import getdefaultlocale, locale_alias

# ContextVars, ambos independientes
_current_lang: ContextVar[str] = ContextVar("_current_lang", default=config.default_lang)
_current_locale: ContextVar[str] = ContextVar("_current_locale", default=config.default_locale)

# Locale context setter, getter and context manager
def _get_system_locale() -> Optional[str]:
    """Return system locale (e.g., 'es_ES', 'en_US')."""
    try:
        lang, _ = getdefaultlocale()
        return lang or None
    except Exception:
        return None

def get_locale() -> str:
    """Return the current locale code from context or system default."""
    try:
        return _current_locale.get()
    except LookupError:
        return _get_system_locale() or config.default_locale

def set_locale(locale_code: str) -> None:
    """Set current locale for this execution context."""
    if config.supported_locales is not None and locale_code not in config.supported_locales:
        raise ValueError(f"Locale '{locale_code}' is not currently supported")
    _current_locale.set(locale_code)

@contextmanager
def use_locale(locale_code: str) -> Generator[None, None, None]:
    """Temporarily set a locale for the current context."""
    token = _current_locale.set(locale_code)
    try:
        yield
    finally:
        _current_locale.reset(token)

# Language context setter, getter and context manager
def get_lang() -> str:
    """Return the current language code from context or default."""
    try:
        return _current_lang.get()
    except LookupError:
        return config.default_lang

def set_lang(lang_code: str) -> None:
    """Set current language for this execution context."""
    if config.supported_langs is not None and lang_code not in config.supported_langs:
        raise ValueError(f"Language '{lang_code}' is not currently supported")
    _current_lang.set(lang_code)

@contextmanager
def use_lang(lang_code: str) -> Generator[None, None, None]:
    """Temporarily set a language for the current context."""
    token = _current_lang.set(lang_code)
    try:
        yield
    finally:
        _current_lang.reset(token)
