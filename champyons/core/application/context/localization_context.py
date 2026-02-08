from contextvars import ContextVar
from contextlib import contextmanager
from datetime import tzinfo
from champyons.core.domain.value_objects.localization import LocalizationContext

_localization_ctx: ContextVar[LocalizationContext] = ContextVar("localization_context", default=LocalizationContext.default())

# Public API
def get_localization_context() -> LocalizationContext:
    return _localization_ctx.get()

def set_localization_context(context: LocalizationContext):
    _localization_ctx.set(context)

@contextmanager
def with_localization_context(context: LocalizationContext):
    token = _localization_ctx.set(context)
    try:
        yield
    finally:
        _localization_ctx.reset(token)

# helpers
def get_current_language() -> str:
    return get_localization_context().language

def get_current_locale() -> str:
    return get_localization_context().locale

def get_current_timezone() -> tzinfo:
    return get_localization_context().timezone