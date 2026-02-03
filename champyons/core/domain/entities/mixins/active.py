from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(kw_only=True)
class ActiveMixin:
    ''' Mixin that adds active (bool) to the entity'''
    active: bool = True