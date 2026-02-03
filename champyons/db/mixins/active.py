from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from champyons.core.timezone.api import now_server

class ActiveMixin:
    """Add an active flag to a model."""
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    def deactivate(self):
        self.active = False
        
    def activate(self):
        self.active = True
        