"""
Continent use cases

This module contains all use cases for continent handling

Submodules:
-----------
- create_from_geonames: handles continent creation from geonames id
- import_all_from_geonames: handles continent creation from geonames, importing all existing continents

Usage:
------
You can import use cases from their specific submodules:

    from champyons.core.application.use_cases.geography.continent.create_from_geonames import CreateContinentFromGeonames
    from champyons.core.application.use_cases.geography.continent.import_all_from_geonames import ImportAllContinentsFromGeonames

Architecture Notes:
-------------------
- TO-DO
"""

# Convenience exports for common entities
# (Uncomment as entities are implemented)
from .create_from_geonames import CreateContinentFromGeonames
from .import_all_from_geonames import ImportAllContinentsFromGeonames

__all__ = [
    "CreateContinentFromGeonames",
    "ImportAllContinentsFromGeonames",
]
