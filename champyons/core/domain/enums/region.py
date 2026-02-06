import enum

class RegionTypeEnum(enum.IntEnum):
    '''
    An enum that represents the type of the region
    '''

    SCOUTABLE_REGION = enum.auto()
    GEOGRAPHIC_REGION = enum.auto()
    TREATY = enum.auto()
