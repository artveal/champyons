from sqlalchemy.types import TypeDecorator, DateTime
from champyons.core.timezone.api import server_tzinfo
from datetime import datetime
from typing import Optional

class UTCDateTime(TypeDecorator):
    """Ensures datetime is stored in the server timezone."""

    impl = DateTime

    def process_bind_param(self, value: Optional[datetime], dialect):
        if value is None:
            return None
        # Make naive datetime aware if needed
        if value.tzinfo is None:
            value = value.replace(tzinfo=server_tzinfo())
        return value.astimezone(server_tzinfo())

    def process_result_value(self, value: Optional[datetime], dialect):
        return value
