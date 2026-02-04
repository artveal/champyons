from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class GeographyMixin:
    ''' Mixin that adds geonames_id (int) to the entity'''
    geonames_id: Optional[int] = None

    