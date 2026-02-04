from sqlalchemy.types import TypeDecorator, DateTime
from datetime import datetime, UTC
from typing import Optional

class UTCDateTime(TypeDecorator):
    """Ensures datetime is stored in the server timezone."""

    impl = DateTime

    def process_bind_param(self, value: Optional[datetime], dialect):
        if value is None:
            return None
        # Make naive datetime aware if needed
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def process_result_value(self, value: Optional[datetime], dialect):
        return value
