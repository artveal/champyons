"""
Geonames API DTOs

Infrastructure DTOs for parsing Geonames API responses.
These are Pydantic models used ONLY in the adapters layer.

The core domain does not know about these - they are converted
to GeographicData (Value Object) before reaching the core.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AlternateNameDTO(BaseModel):
    """
    Alternate name from Geonames API.
    
    Represents a name in a different language or variant of the main name.
    """
    name: str
    lang: Optional[str] = None
    is_short_name: bool = Field(default=False, alias="isShortName")
    is_preferred_name: bool = Field(default=False, alias="isPreferredName")
    is_historical: bool = Field(default=False, alias="isHistorical")
    is_colloquial: bool = Field(default=False, alias="isColloquial")
    
    class Config:
        populate_by_name = True  # Allow both snake_case and camelCase


class GeonamesTimezoneDTO(BaseModel):
    """Timezone information from Geonames API"""
    gmt_offset: Optional[float] = Field(default=None, alias="gmtOffset")
    timezone_id: Optional[str] = Field(default=None, alias="timeZoneId")
    dst_offset: Optional[float] = Field(default=None, alias="dstOffset")
    
    class Config:
        populate_by_name = True


class GeonamesBBoxDTO(BaseModel):
    """Bounding box coordinates from Geonames API"""
    east: float = 0.0
    south: float = 0.0
    north: float = 0.0
    west: float = 0.0
    accuracy_level: Optional[int] = Field(default=None, alias="accuracyLevel")
    
    class Config:
        populate_by_name = True


class GeonamesResultDTO(BaseModel):
    """
    Full Geonames API response DTO (style="full").
    
    This is an infrastructure DTO used ONLY in the adapters layer.
    It parses the raw JSON from Geonames API.
    
    The adapter converts this to GeographicData (domain Value Object)
    before passing to the core.
    
    Field naming follows Geonames API conventions (camelCase),
    with aliases for Python snake_case.
    """
    
    # ===== Core fields (always present) =====
    
    geoname_id: int = Field(alias="geonameId")
    name: str
    toponym_name: str = Field(alias="toponymName")
    lng: float
    lat: float
    fcl: str  # Feature class (A, P, H, etc.)
    fcode: str  # Feature code (PCLI, PPL, etc.)
    
    # ===== Country fields =====
    
    country_id: Optional[int] = Field(default=None, alias="countryId")
    country_code: Optional[str] = Field(default=None, alias="countryCode")
    country_name: Optional[str] = Field(default=None, alias="countryName")
    cc2: Optional[str] = None  # Alternative country codes
    
    # ===== Population and geography =====
    
    population: Optional[int] = None
    elevation: Optional[int] = None
    dem: Optional[int] = None  # Digital elevation model
    astergdem: Optional[int] = None
    srtm3: Optional[int] = None
    
    # ===== Administrative divisions =====
    
    admin_code1: Optional[str] = Field(default=None, alias="adminCode1")
    admin_code2: Optional[str] = Field(default=None, alias="adminCode2")
    admin_code3: Optional[str] = Field(default=None, alias="adminCode3")
    admin_code4: Optional[str] = Field(default=None, alias="adminCode4")
    admin_code5: Optional[str] = Field(default=None, alias="adminCode5")
    
    admin_name1: Optional[str] = Field(default=None, alias="adminName1")
    admin_name2: Optional[str] = Field(default=None, alias="adminName2")
    admin_name3: Optional[str] = Field(default=None, alias="adminName3")
    admin_name4: Optional[str] = Field(default=None, alias="adminName4")
    admin_name5: Optional[str] = Field(default=None, alias="adminName5")
    
    admin_id1: Optional[int] = Field(default=None, alias="adminId1")
    admin_id2: Optional[int] = Field(default=None, alias="adminId2")
    admin_id3: Optional[int] = Field(default=None, alias="adminId3")
    admin_id4: Optional[int] = Field(default=None, alias="adminId4")
    admin_id5: Optional[int] = Field(default=None, alias="adminId5")
    
    admin_codes1: dict[str, str] = Field(default_factory=dict, alias="adminCodes1")
    admin_type_name: Optional[str] = Field(default=None, alias="adminTypeName")
    
    # ===== Feature names =====
    
    fcl_name: Optional[str] = Field(default=None, alias="fclName")
    fcode_name: Optional[str] = Field(default=None, alias="fcodeName")
    ascii_name: Optional[str] = Field(default=None, alias="asciiName")
    
    # ===== Continent =====
    
    continent_code: Optional[str] = Field(default=None, alias="continentCode")
    
    # ===== Timezone =====
    
    timezone: Optional[GeonamesTimezoneDTO] = None
    
    # ===== Bounding box =====
    
    bbox: Optional[GeonamesBBoxDTO] = None
    
    # ===== Alternate names =====
    
    alternate_names: list[AlternateNameDTO] = Field(
        default_factory=list,
        alias="alternateNames"
    )
    
    # ===== Search metadata =====
    
    score: Optional[float] = None  # Search relevance score
    
    # ===== External links =====
    
    wikipedia_url: Optional[str] = Field(default=None, alias="wikipediaURL")
    
    class Config:
        populate_by_name = True  # Allow both camelCase and snake_case
        extra = "allow"  # Allow extra fields from API without errors
    
    @field_validator("fcl", mode="before")
    @classmethod
    def validate_fcl(cls, v: str) -> str:
        """Ensure feature class is uppercase single letter"""
        if v:
            return v.upper()
        return v
    
    @field_validator("fcode", mode="before")
    @classmethod
    def validate_fcode(cls, v: str) -> str:
        """Ensure feature code is uppercase"""
        if v:
            return v.upper()
        return v
    
    # ===== Helper methods =====
    def get_all_translations(self, language: str, *, include_short: bool = True, include_colloquial: bool = False, include_historical: bool = False) -> list[str]:
        """
        Get all names in a specific language.
        
        Returns list ordered by: preferred, short, colloquial, historical, others
        """
        names_by_priority = {
            "preferred": [],
            "short": [],
            "colloquial": [],
            "historical": [],
            "other": []
        }
        
        for alt_name in self.alternate_names:
            if alt_name.lang != language:
                continue
            
            if alt_name.is_preferred_name:
                names_by_priority["preferred"].append(alt_name.name)
            elif alt_name.is_short_name:
                names_by_priority["short"].append(alt_name.name)
            elif alt_name.is_colloquial:
                names_by_priority["colloquial"].append(alt_name.name)
            elif alt_name.is_historical:
                names_by_priority["historical"].append(alt_name.name)
            else:
                names_by_priority["other"].append(alt_name.name)
        
        # Flatten in priority order
        translations = names_by_priority["preferred"]
        if include_short:
            translations += names_by_priority["short"]
        if include_colloquial:
            translations += names_by_priority["colloquial"]
        if include_historical:
            translations += names_by_priority["historical"]
        translations += names_by_priority["other"]
        return translations


class GeonamesSearchResponseDTO(BaseModel):
    """
    Response from Geonames search endpoint.
    
    Contains total results count and list of geonames.
    """
    total_results_count: int = Field(alias="totalResultsCount")
    geonames: list[GeonamesResultDTO] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True


class GeonamesErrorDTO(BaseModel):
    """
    Error response from Geonames API.
    
    Example:
    {
        "status": {
            "message": "user account not enabled to use this service",
            "value": 18
        }
    }
    """
    message: str
    value: int
    
    class Config:
        populate_by_name = True