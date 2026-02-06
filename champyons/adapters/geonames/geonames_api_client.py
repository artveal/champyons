"""
Geonames API Client

Adapter that fetches data from Geonames HTTP API and converts
it to domain Value Objects.

This adapter:
1. Makes HTTP requests to Geonames
2. Parses JSON into Pydantic DTOs (infrastructure layer)
3. Converts DTOs to GeographicData (domain layer)
"""

import requests
from typing import Optional
from pydantic import ValidationError

from champyons.core.domain.value_objects.geonames import GeonamesData, GeonamesFeatureClass, GeonamesFeatureCode
from champyons.core.services.geonames_service import GeonamesRepository
from .dto import (
    GeonamesResultDTO,
    GeonamesSearchResponseDTO,
    GeonamesErrorDTO
)


class GeonamesClient(GeonamesRepository):
    """
    Client for Geonames HTTP API.
    
    Configuration:
        - Base URL: http://api.geonames.org
        - Requires username (free account at geonames.org)
        - Rate limit: 20,000 requests/day (free tier)
        - 2,000 requests/hour
    
    Usage:
        client = GeonamesClient(username="your_username")
        
        # Fetch single entity
        geo_data = client.fetch_by_id(2510769)  # Spain
        
        # Search
        results = client.search_by_query(name="Barcelona", fclass="P")
    """
    
    BASE_URL = "http://api.geonames.org"
    
    def __init__(self, username: str, *, timeout: int = 10, style: str = "full", supported_languages_for_translations: list[str]|None = None, include_short_translations: bool = True, include_colloquial_translations: bool = False, include_historical_translations: bool = False):
        """
        Initialize Geonames client.
        
        Args:
            username: Geonames username (register at geonames.org)
            timeout: Request timeout in seconds. Defaults to 10
            style: Response style ("short", "medium", "full"). Defaults to "full"
            supported_languages_for_translations: list of languages from which translations will be gathered (in-game available languages)
            include_short_translations: include short version for translated names. Defaults to True
            include_colloquial_translations: include colloquial version for translated names. Defaults to False
            include_historical_translations: include historical version for translated names. Defaults to False 
        """
        if not username:
            raise ValueError("Geonames username is required")
        
        self.username = username
        self.timeout = timeout
        self.style = style
        self.supported_languages = supported_languages_for_translations or list()

    
    # ===== Public API =====
    
    def fetch_by_id(self, geoname_id: int) -> GeonamesData:
        """
        Fetch geographic entity by Geonames ID.
        
        Args:
            geoname_id: Geonames identifier
            include_translations: Whether to process alternate names
            
        Returns:
            GeonamesData value object
            
        Raises:
            GeonamesNotFoundError: If ID doesn't exist
            GeonamesAPIError: If API call fails
        """
        # 1. Call API
        dto = self._fetch_from_api("getJSON", geoname_id)
        
        # 2. Convert to domain VO
        return self._to_geographic_data(dto)
    

    def search_by_query(self, **query_params) -> list[GeonamesData]:
        """
        Search for geographic entities by query parameters
            
        Returns:
            List of GeographicData value objects
        """
        # 1. Call search API
        dtos = self._search_api("searchJson", **query_params)
        
        # 2. Convert all to domain VOs
        return [self._to_geographic_data(dto) for dto in dtos]
    
    def search_children(self, parent_id, **query_params) -> list[GeonamesData]:
        """
        Search for geographic entities that are children of given geonames id
        
        Args:
            parent_id: geonames id for parent record from which children will be searched
            
        Returns:
            List of GeographicData value objects
        """
        # 1. Call search API
        dtos = self._search_api("childrenJSON", geonameId=parent_id, **query_params)
        
        # 2. Convert all to domain VOs
        return [self._to_geographic_data(dto) for dto in dtos]


    # ===== Private: API Calls =====
    
    def _fetch_from_api(self, endpoint: str, geoname_id: int, **query_params) -> GeonamesResultDTO:
        """
        Fetch single entity from Geonames API.
        
        """
        url = f"{self.BASE_URL}/{endpoint}"
        query_params["username"] = self.username
        query_params["style"] = self.style
        
        try:
            response = requests.get(url, params=query_params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "status" in data:
                error = GeonamesErrorDTO(**data["status"])
                if error.value == 15:  # Not found
                    raise ValueError(
                        f"Geonames ID {geoname_id} not found"
                    )
                raise RuntimeError(f"Geonames API error: {error.message}")
            
            # Parse into Pydantic DTO
            return GeonamesResultDTO(**data)
            
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch from Geonames: {e}")
        except ValidationError as e:
            raise ValidationError(f"Failed to parse Geonames response: {e}")
    
    def _search_api(
        self,
        endpoint: str,
        **query_params
    ) -> list[GeonamesResultDTO]:
        """
        Search Geonames API.
        
        Endpoint: /searchJSON
        """
        url = f"{self.BASE_URL}/{endpoint}"
        query_params["username"] = self.username
        query_params["style"] = self.style
        
        
        try:
            response = requests.get(url, params=query_params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "status" in data:
                error = GeonamesErrorDTO(**data["status"])
                raise RuntimeError(f"Geonames API error: {error.message}")
            
            # Parse search response
            search_response = GeonamesSearchResponseDTO(**data)
            return search_response.geonames
            
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to search Geonames: {e}")
        except ValidationError as e:
            raise ValidationError(f"Failed to parse Geonames response: {e}")
    
    # ===== Private: DTO → Domain Conversion =====
    
    def _to_geographic_data(
        self,
        dto: GeonamesResultDTO,
    ) -> GeonamesData:
        """
        Convert Geonames DTO (infrastructure) to GeographicData (domain).
        
        This is the boundary between infrastructure and domain layers.
        
        Args:
            dto: Parsed Pydantic DTO from API
            include_translations: Whether to process alternate names
            
        Returns:
            Domain Value Object
        """
        # Process translations if requested
        translations = {}

        # Get preferred names in common languages
        for lang in self.supported_languages:
            preferred = dto.get_all_translations(lang)
            if preferred and preferred[0] != dto.name:
                translations[lang] = preferred[0]
        
        # Create domain Value Object
        return GeonamesData(
            geonames_id=dto.geoname_id,
            name=dto.name,
            country_code=dto.country_code,
            other_country_codes=[code.strip() for code in dto.cc2.split(",")] if dto.cc2 else [],
            continent_code=dto.continent_code,
            feature_class=GeonamesFeatureClass(dto.fcl),
            feature_code=GeonamesFeatureCode(dto.fcode),
            population=dto.population or 0,
            latitude=dto.lat,
            longitude=dto.lng,
            elevation=dto.elevation,
            timezone_id=dto.timezone.timezone_id if dto.timezone else None,
            translations=translations
        )
