from dataclasses import dataclass, field
from datetime import datetime, UTC

now_server = lambda: datetime.now(UTC) # define a lambda function for returning current time in UTC (server time)

@dataclass(kw_only=True)
class TimestampMixin:
    ''' Mixin that adds created_at and updated_at (datetime) to the entity'''
    created_at: datetime = field(default_factory=now_server)
    updated_at: datetime = field(default_factory=now_server)

    def update_timestamp(self) -> None:
        self.updated_at = now_server()