from dataclasses import dataclass, field
from typing import Optional, Dict
import json
from ..enums.geonames import FeatureClass, FeatureCode

def normalize_fclass(v: str | FeatureClass) -> FeatureClass:
    if isinstance(v, str):
        v = v.upper()
    else:
        return v
    try:
        return FeatureClass[v]
    except ValueError:
        return FeatureClass.A

def normalize_fcode(v: str | FeatureCode) -> FeatureCode:

    if isinstance(v, str):
        v = v.upper()
    else:
        return v

    try:
        return FeatureCode[v]
    except ValueError:
        return FeatureCode.NULL

@dataclass(frozen=True)
class AlternateName:
    name: str
    lang: str|None = None
    isShortName: bool = False
    isPreferredName: bool = False
    isHistorical: bool = False
    isColloquial: bool = False

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> "AlternateName":
        return cls(
            name= data["name"],
            lang= data.get("lang"),
            isShortName= data.get("isShortName", False),
            isPreferredName= data.get("isPreferredName", False),
            isHistorical= data.get("isHistorical", False),
            isColloquial= data.get("isColloquial", False)
        )
    

@dataclass(frozen=True)
class GeonamesTimezone:
    gmtOffset: Optional[int] = None
    timeZoneId: Optional[str] = None
    dstOffset: Optional[int] = None

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> "GeonamesTimezone":
        return cls(**data)

@dataclass(frozen=True)
class GeonamesBBox:
    east: float = 0.0
    south: float = 0.0
    north: float = 0.0
    west: float = 0.0
    accuracyLevel: Optional[int] = None

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> "GeonamesBBox":
        return cls(**data)

@dataclass(frozen=True)
class GeonamesResult:
    # Short/Medium/Full
    geonameId: int
    name: str
    toponymName: str
    lng: float
    lat: float
    fcl: FeatureClass
    fcode: FeatureCode
    countryId: int | None = None
    countryCode: str | None = None

    # Medium fields
    cc2: Optional[str] = None
    population: Optional[int] = None
    countryName: Optional[str] = None
    adminCode1: Optional[str] = None
    adminName1: Optional[str] = None
    adminId1: Optional[int] = None
    adminCodes1: Dict[str, str] = field(default_factory=dict)
    fclName: Optional[str] = None
    fcodeName: Optional[str] = None

    # Full fields
    timezone: Optional[GeonamesTimezone] = None
    bbox: Optional[GeonamesBBox] = None
    asciiName: Optional[str] = None
    elevation: Optional[int] = None
    astergdem: Optional[int] = None
    srtm3: Optional[int] = None
    score: Optional[float] = None
    continentCode: Optional[str] = None
    adminTypeName: Optional[str] = None
    
    adminId2: Optional[int] = None
    adminId3: Optional[int] = None
    adminId4: Optional[int] = None
    adminId5: Optional[int] = None
    adminCode2: Optional[str] = None
    adminCode3: Optional[str] = None
    adminCode4: Optional[str] = None
    adminCode5: Optional[str] = None
    adminName2: Optional[str] = None
    adminName3: Optional[str] = None
    adminName4: Optional[str] = None
    adminName5: Optional[str] = None

    wikipediaURL: Optional[str] = None
    alternateNames: list[AlternateName] = field(default_factory=list)

    def __post_init__(self):
        object.__setattr__(self, "fcl", normalize_fclass(self.fcl))
        object.__setattr__(self, "fcode", normalize_fcode(self.fcode))

    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        if self.timezone:
            data["timezone"] = self.timezone.to_dict()
        if self.bbox:
            data["bbox"] = self.bbox.to_dict()
        if self.alternateNames:
            data["alternateNames"] = [alt_name.to_dict() for alt_name in self.alternateNames]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "GeonamesResult":
        tz = GeonamesTimezone.from_dict(data["timezone"]) if data.get("timezone") else None
        bbox = GeonamesBBox.from_dict(data["bbox"]) if data.get("bbox") else None
        alt_names = [AlternateName.from_dict(alt_name) for alt_name in data["alternateNames"]]
        return cls(
            **{k: v for k, v in data.items() if k not in ("timezone", "bbox", "alternateNames")},
            timezone=tz,
            bbox=bbox,
            alternateNames=alt_names
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, s: str) -> "GeonamesResult":
        return cls.from_dict(json.loads(s))