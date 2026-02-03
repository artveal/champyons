from typing import Optional
import enum

class CityPopulationRange(enum.IntEnum):
    '''
    City population ranges. Metadata for lower and upper limit is configured via min_population and max_population attributes
    '''
    min_population: Optional[int]
    max_population: Optional[int]

    UNSET =                     (0, None, None)
    FROM_0_TO_1000 =            (1, 0, 1_000)
    FROM_1001_TO_2500 =         (2, 1_001, 2_500)
    FROM_2501_TO_5000 =         (3, 2_501, 5_000)
    FROM_5001_TO_10000 =        (4, 5_001, 10_000)
    FROM_10001_TO_25000 =       (5, 10_001, 25_000)
    FROM_25001_TO_50000 =       (6, 25_001, 50_000)
    FROM_50001_TO_100000 =      (7, 50_001, 100_000)
    FROM_100001_TO_250000 =     (8, 100_001, 250_000)
    FROM_250001_TO_500000 =     (9, 250_001, 500_000)
    FROM_500001_TO_1000000 =    (10, 500_001, 1_000_000)
    FROM_1000001_TO_2500000 =   (11, 1_000_001, 2_500_000)
    FROM_2500001_TO_5000000 =   (12, 2_500_001, 5_000_000)
    FROM_5000001_TO_10000000 =  (13, 5_000_001, 10_000_000)
    FROM_10000001_TO_20000000 = (14, 10_000_001, 20_000_000)
    MORE_THAN_20000000 =        (15, 20_000_001, None)

    def __new__(cls, value: int, min_population: Optional[int], max_population: Optional[int]):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.min_population = min_population
        obj.max_population = max_population
        return obj
    
    @classmethod
    def from_population(cls, population: int) -> 'CityPopulationRange':
        if not isinstance(population, int) or population < 0:
            return cls.UNSET
        for r in cls:
            if r.min_population is not None and population < r.min_population:
                continue
            if r.max_population is not None and population > r.max_population:
                continue
            return r
        return cls.UNSET