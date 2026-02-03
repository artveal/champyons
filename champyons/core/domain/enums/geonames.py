from typing import Optional
from enum import StrEnum, auto

class FeatureClass(StrEnum):
    description: str|None

    A =  auto(), "country, state, region,..."
    H =  auto(), "stream, lake, ..."
    L =  auto(), "parks,area, ..."
    P =  auto(), "city, village,..."
    R =  auto(), "road, railroad" 
    S =  auto(), "spot, building, farm"
    T =  auto(), "mountain,hill,rock,..." 
    U =  auto(), "undersea"
    V =  auto(), "forest,heath,..."

    def __new__(cls, value: str, description: Optional[str]):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

class FeatureCode(StrEnum):
    feature_class: FeatureClass|None
    description: str|None
    
    CONT    =   auto(), FeatureClass.L, "continent"
    ADM1	=	auto(), FeatureClass.A,	"first-order administrative division"
    ADM1H	=	auto(), FeatureClass.A,	"historical first-order administrative division"
    ADM2	=	auto(), FeatureClass.A,	"second-order administrative division"
    ADM2H	=	auto(), FeatureClass.A,	"historical second-order administrative division"
    ADM3	=	auto(), FeatureClass.A,	"third-order administrative division"
    ADM3H	=	auto(), FeatureClass.A,	"historical third-order administrative division"
    ADM4	=	auto(), FeatureClass.A,	"fourth-order administrative division"
    ADM4H	=	auto(), FeatureClass.A,	"historical fourth-order administrative division"
    ADM5	=	auto(), FeatureClass.A,	"fifth-order administrative division"
    ADM5H	=	auto(), FeatureClass.A,	"historical fifth-order administrative division"
    ADMD	=	auto(), FeatureClass.A,	"administrative division"
    ADMDH	=	auto(), FeatureClass.A,	"historical administrative division "
    ADMS	=	auto(), FeatureClass.A,	"school district"
    LTER	=	auto(), FeatureClass.A,	"leased area"
    PCL	    =	auto(), FeatureClass.A,	"political entity"
    PCLD	=	auto(), FeatureClass.A,	"dependent political entity"
    PCLF	=	auto(), FeatureClass.A,	"freely associated state"
    PCLH	=	auto(), FeatureClass.A,	"historical political entity"
    PCLI	=	auto(), FeatureClass.A,	"independent political entity"
    PCLIX	=	auto(), FeatureClass.A,	"section of independent political entity"
    PCLS	=	auto(), FeatureClass.A,	"semi-independent political entity"
    PRSH	=	auto(), FeatureClass.A,	"parish"
    TERR	=	auto(), FeatureClass.A,	"territory"
    ZN	    =	auto(), FeatureClass.A,	"zone"
    ZNB	    =	auto(), FeatureClass.A,	"buffer zone"
    PPL	    =	auto(), FeatureClass.P,	"populated place"
    PPLA	=	auto(), FeatureClass.P,	"seat of a first-order administrative division"
    PPLA2	=	auto(), FeatureClass.P,	"seat of a second-order administrative division"
    PPLA3	=	auto(), FeatureClass.P,	"seat of a third-order administrative division"
    PPLA4	=	auto(), FeatureClass.P,	"seat of a fourth-order administrative division"
    PPLA5	=	auto(), FeatureClass.P,	"seat of a fifth-order administrative division"
    PPLC	=	auto(), FeatureClass.P,	"capital of a political entity"
    PPLCD	=	auto(), FeatureClass.P,	"capital of a dependency or special area"
    PPLCH	=	auto(), FeatureClass.P,	"historical capital of a political entity"
    PPLF	=	auto(), FeatureClass.P,	"farm village"
    PPLG	=	auto(), FeatureClass.P,	"seat of government of a political entity"
    PPLH	=	auto(), FeatureClass.P,	"historical populated place"
    PPLL	=	auto(), FeatureClass.P,	"populated locality"
    PPLQ	=	auto(), FeatureClass.P,	"abandoned populated place"
    PPLR	=	auto(), FeatureClass.P,	"religious populated place"
    PPLS	=	auto(), FeatureClass.P,	"populated places"
    PPLW	=	auto(), FeatureClass.P,	"destroyed populated place"
    PPLX	=	auto(), FeatureClass.P,	"section of populated place"
    STLMT	=	auto(), FeatureClass.P,	"israeli settlement"
    
    NULL	=	auto(), None, "not available"

    def __new__(cls, value: str, feature_class: Optional[FeatureClass], description: Optional[str]):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.feature_class = feature_class
        obj.description = description
        return obj