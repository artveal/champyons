from dataclasses import dataclass, field
from datetime import datetime

from champyons.core.timezone import now_server

@dataclass(kw_only=True)
class TimestampMixin:
    ''' Mixin that adds created_at and updated_at (datetime) to the entity'''
    created_at: datetime = field(default_factory=now_server)
    updated_at: datetime = field(default_factory=now_server)