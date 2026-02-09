from champyons.core.domain.entities import Country, LocalRegion, City, Nationality
from champyons.core.domain.value_objects.geography.culture import Culture
from typing import List, Optional
from dataclasses import dataclass

import random

@dataclass
class PlayerGenerationContext:
    """Context data for player generation."""
    residence_city: City
    residence_local_region: Optional[LocalRegion]
    residence_nation: Country
    nationality: Nationality
    culture: Culture
    is_indigenous: bool
    secondary_nationalities: List[Nationality]

class PlayerGenerator:
    
    def generate_player_context(self, club_base_nation: Country | LocalRegion) -> PlayerGenerationContext:
        """Generate complete player context."""
        
        # Step 1: Select city by population
        residence_city = self._select_city_by_population(club_base_nation)
        
        # Step 2: Get nationality from city's local region or nation
        primary_nationality = self._get_nationality_from_city(residence_city, club_base_nation)
        
        # Step 3: Determine if indigenous
        is_indigenous = self._is_indigenous(primary_nationality, residence_city, club_base_nation)
        
        # Step 4: Select culture
        if primary_nationality.culture_distribution is None:
            raise ValueError(f"Nationality {primary_nationality.name} has no culture_distribution")
        
        culture = primary_nationality.culture_distribution.get_random_culture()
        
        # Step 5: Handle secondary nationalities
        secondary_nationalities = self._determine_secondary_nationalities(
            primary_nationality=primary_nationality,
            is_indigenous=is_indigenous,
            residence_city=residence_city,
            club_base_nation=club_base_nation
        )
        
        return PlayerGenerationContext(
            residence_city=residence_city,
            residence_local_region=residence_city.local_region,
            residence_nation=self._get_nation(club_base_nation),
            nationality=primary_nationality,
            culture=culture,
            is_indigenous=is_indigenous,
            secondary_nationalities=secondary_nationalities
        )
    
    def _select_city_by_population(self, club_base_nation: Country|LocalRegion):
        """Select a city weighted by population."""
        cities = club_base_nation.cities
        
        if not cities:
            raise ValueError(f"No cities found in {club_base_nation.name}")
        
        # Weight by population
        weights = [city.population for city in cities]
        return random.choices(cities, weights=weights, k=1)[0]
    
    def _get_nationality_from_city(self, city: City, club_base: Country|LocalRegion) -> Nationality:
        """
        Get nationality following hierarchy:
        1. City's local region (if exists)
        2. Nation
        """
        local_region = city.local_region
        
        if local_region:
            return local_region.get_random_nationality()
        else:
            nation = self._get_nation(club_base)
            return nation.get_random_nationality()
    
    def _is_indigenous(self, nationality: Nationality, city: City, club_base: Country | LocalRegion) -> bool:
        """Determine if nationality is indigenous to the residence area."""
        local_region = city.local_region
        
        # Check local region first
        if local_region:
            if local_region.is_indigenous_nationality(nationality):
                return True
        
        # Check nation
        nation = self._get_nation(club_base)
        return nation.is_indigenous_nationality(nationality)
    
    def _get_nation(self, club_base: Country | LocalRegion) -> Country:
        """Get the nation from club_base (either directly or from local region)."""
        if isinstance(club_base, Country):
            return club_base
        else:  # LocalRegion
            if not club_base.nation:
                raise ValueError(f"LocalRegion {club_base.name} has no associated nation")
            return club_base.nation
        
    def _determine_secondary_nationalities(self, primary_nationality: Nationality, is_indigenous: bool, residence_city: City, club_base_nation: Country | LocalRegion) -> List[Nationality]:
        """Determine additional nationalities."""
        secondary = []
        
        # Rule 1: Indigenous from local region also gets nation nationality
        if is_indigenous and residence_city.local_region:
            local_region = residence_city.local_region
            nation = local_region.nation
            
            if (local_region.nationality and 
                primary_nationality == local_region.nationality and
                nation and nation.nationality and
                nation.nationality != primary_nationality):
                secondary.append(nation.nationality)
        
        # Rule 2: Foreign players may acquire residence nationality
        if not is_indigenous:
            residence_nationality = self._get_residence_nationality(club_base_nation)
            if residence_nationality and residence_nationality != primary_nationality:
                if self._simulate_nationality_acquisition(primary_nationality, residence_nationality):
                    secondary.append(residence_nationality)
        
        return secondary
    
    def _get_residence_nationality(self, club_base: Country | LocalRegion) -> Optional[Nationality]:
        """Get the nationality of residence (club_base)."""
        return club_base.nationality
        
    def _simulate_nationality_acquisition(self, origin: Nationality, residence: Nationality) -> bool:
        """Simulate if foreign player acquires residence nationality."""
        years = random.randint(1, 15)
        
        if not residence.nationality_rules:
            return False
        
        # You'll implement this based on your NationalityRules
        # For now, simple rule: 5+ years = eligible
        return years >= 5