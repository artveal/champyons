from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional

from champyons.core.ports.services.localization_service import LocalizationService
from champyons.core.application.context.localization_context import get_localization_context
from champyons.core.domain.value_objects.localization import LazyString

class LocalizationManager:
    def __init__(self, service: LocalizationService):
        self.service = service

    # translations
    def translate(self, key: str, **kwargs) -> str:
        ctx = get_localization_context()
        return self.service.translate(key, ctx, **kwargs)
    
    def lazy_translate(self, key: str, **kwargs) -> LazyString:
        ctx = get_localization_context()
        return LazyString(lambda: self.service.translate(key, ctx, **kwargs))
    
    # formatters
    def format_number(self, value: int|float|Decimal, decimal_places: Optional[int] = None, use_group_separator: bool = True) -> str:
        ctx = get_localization_context()
        return self.service.format_number(value, ctx, decimal_places, use_group_separator)

    def format_currency(self, amount: int, compact: bool = False, decimal_places: int = 0):
        ctx = get_localization_context()
        if compact:
            return self.service.format_compact_currency(amount, ctx, decimal_places=decimal_places)
        return self.service.format_currency(amount, ctx)