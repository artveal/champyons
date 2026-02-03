from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from champyons.core.timezone.api import now_server
from ..types import UTCDateTime

class TimestampMixin:
    """Add created_at and updated_at timestamps to a model."""
    
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime,
        default=now_server
    )

    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime,
        default=now_server,
        onupdate=now_server
    )
