"""
Entity domains module.

Adds useful attributes, properties and/or methods to entities of each module

Mixins:
-----------
- active: enables soft-deletion
- author: adds support for user creation/modification
- geography: adds geonames_id to geogrephic entities, and therefore can be syncronized via api.geonames
- timestamp: adds support for creation and modification datetimes

Usage:
------
You can import mixins each mixin individually:

    from champyons.core.domain.entities.mixins.active import ActiveMixin
    from champyons.core.domain.entities.mixins.author import AuthorMixin
    from champyons.core.domain.entities.mixins.geography import GeographyMixin
    from champyons.core.domain.entities.mixins.timestamp import TimestampMixin

Or import then from here:

    from champyons.core.domain.entities.mixins import ActiveMixin, GeographyMixin
"""

# Import mixins for easy access
from .active import ActiveMixin
from .author import AuthorMixin
from .geography import GeographyMixin
from .timestamp import TimestampMixin

__all__ = [
    "ActiveMixin",
    "AuthorMixin",
    "GeographyMixin", 
    "TimestampMixin"
]
