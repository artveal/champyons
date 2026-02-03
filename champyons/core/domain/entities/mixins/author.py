from dataclasses import dataclass, field
from typing import Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..user import User

@dataclass(kw_only=True)
class AuthorMixin:
    ''' Mixin that adds optional created_by and updated_by (User instances) and created_by_id and updated_by_id (Optional[int]) to the entity'''
    created_by_id: Optional[int] = None
    updated_by_id: Optional[int] = None

    created_by: Optional["User"] = None  # forward reference, only memory
    updated_by: Optional["User"] = None