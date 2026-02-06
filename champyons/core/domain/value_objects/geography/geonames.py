from dataclasses import dataclass, field
from typing import Optional
from enum import StrEnum

class GeonamesFeatureClass(StrEnum):
    A =  "A" # country, state, region,...
    H =  "H" # stream, lake, ...
    L =  "L" # parks,area, ...
    P =  "P" # city, village...
    R =  "R" # roads
    S =  "S" # spots (buildings, farms...)
    T =  "T" # terrain (mountains, hills...)
    U =  "U" # undersea
    V =  "V" # forest

class GeonamesFeatureCode(StrEnum):
    # supra-national entities (continents, regions, zones...)
    CONTINENT = "CONT"
    ZONE = "ZN"
    BUFFER_ZONE = "ZNB"
    REGION = "RGN"
    ECONOMIC_REGION = "RGNE"
    
    # political entities (nations)
    POLITICAL_ENTITY = "PCL"
    DEPENDENT_POLITICAL_ENTITY = "PCLD"
    FREELY_ASSOCIATED_STATE	= "PCLF"
    INDEPENDANT_POLITICAL_ENTITY = "PCLI"
    INDEPENDANT_POLITICAL_ENTITY_SECTION = "PCLIX"
    SEMI_INDEPENDANT_POLITICAL_ENTITY =	"PCLS"
    
    # subnational administrative entities
    ADMIN_1	= "ADM1"
    ADMIN_2	= "ADM2"
    ADMIN_3	= "ADM3"
    ADMIN_4	= "ADM4"
    ADMIN_5	= "ADM5"
    ADMIN_DIVISION	= "ADMD"
    LEASED_AREA	=	"LTER"
    PARISH	=	"PRSH"
    TERRITORY	=	"TERR"
    
    # populated places (towns and cities)
    POPULATED_PLACE	= "PPL"
    POLITICAL_ENTITY_CAPITAL = "PPLC"
    SEAT_OF_GOVERMENT =	"PPLG"
    SEAT_OF_ADMIN_1	= "PPLA"
    SEAT_OF_ADMIN_2	= "PPLA2"
    SEAT_OF_ADMIN_3	= "PPLA3"
    SEAT_OF_ADMIN_4	= "PPLA4"
    SEAT_OF_ADMIN_5	= "PPLA5"

    FARM_VILLAGE	= "PPLF"
    POPULATED_LOCALITY	= "PPLL"
    RELIGIUS_POPULATED_PLACE	= "PPLR"
    POPULATED_PLACES	= "PPLS"
    SECTION_OF_POPULATED_PLACE	= "PPLX"
    ISRAELI_SETTLEMENT	= "STLMT"

    # historical, destroyed or abandoned
    HISTORICAL_REGION = "RGNH"
    HISTORICAL_POLITICAL_ENTITY	= "PCLH"
    HISTORICAL_ADMIN_1 = "ADM1H"
    HISTORICAL_ADMIN_2 = "ADM2H"
    HISTORICAL_ADMIN_3 = "ADM3H"
    HISTORICAL_ADMIN_4 = "ADM4H"
    HISTORICAL_ADMIN_5 = "ADM5H"
    HISTORICAL_ADMIN_DIVISION	= "ADMDH"
    HISTORICAL_CAPITAL	= "PPLCH"
    HISTORICAL_POPULATED_PLACE	= "PPLH"
    ABANDONED_POPULATED_PLACE	="PPLQ"
    DESTROYED_POPULATED_PLACE	= "PPLW"
  
    # unset
    NULL	=	"NULL"

ALLOWED_FCODES_FOR_LOCAL_REGIONS = {
    "ADM1", "ADM2", "ADM3", "ADM4", "ADM5", "ADMD", "LTER", "PRSH", "TERR", "RGN",
    "RGNH", "ADM1H", "ADM2H", "ADM3H", "ADM4H", "ADM5H", "ADMDH"
}
ALLOWED_FCODES_FOR_NATIONS = ALLOWED_FCODES_FOR_LOCAL_REGIONS.union({"PCL", "PCLD", "PCLF",
                                                                     "PCLI", "PCLIX", "PCLS",
                                                                     "PCLH"})
                                                                     
ALLOWED_FCODES_FOR_CITIES = {"PPL", "PPLC", "PPLG" "PPLA", "PPLA2", "PPLA3",
                             "PPLA4", "PPLA5", "PPLF", "PPLL", "PPLR", "PPLS",
                             "PPLX", "STLMT", "PPLH", "PPLCH", "PPLQ", "PPLW"}

ALLOWED_FCODES_FOR_CONTINENTS = {"CONT"}
ALLOWED_FCODES_FOR_REGIONS = {"ZN", "CONT", "RGN", "RGNE", "RGNH"}


@dataclass(frozen=True)
class GeonamesData:
    geonames_id: int
    name: str
    feature_class: GeonamesFeatureClass
    feature_code: GeonamesFeatureCode
    
    longitude: float
    latitude: float
    elevation: Optional[int] = None

    population: int = 0

    country_code: Optional[str] = None
    other_country_codes: list[str] = field(default_factory=list)
    continent_code: Optional[str] = None
    timezone_id: Optional[str] = None
    translations: dict[str, str] = field(default_factory=dict)

    @property
    def can_be_continent(self) -> bool:
        """ Returns whether the instance can be a continent"""
        return self.feature_code.value in ALLOWED_FCODES_FOR_CONTINENTS
    
    @property
    def can_be_region(self) -> bool:
        """ Returns whether the instance can be a region"""
        return self.feature_code.value in ALLOWED_FCODES_FOR_REGIONS
    
    @property
    def can_be_nation(self) -> bool:
        """ Returns whether the instance can be a nation"""
        return self.feature_code.value in ALLOWED_FCODES_FOR_NATIONS
    
    @property
    def can_be_local_region(self) -> bool:
        """ Returns whether the instance can be a local region"""
        return self.feature_code.value in ALLOWED_FCODES_FOR_LOCAL_REGIONS
    
    @property
    def can_be_city(self) -> bool:
        """ Returns whether the instance can be a city/town"""
        return self.feature_code.value in ALLOWED_FCODES_FOR_CITIES