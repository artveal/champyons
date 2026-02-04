from champyons.core.domain.value_objects.geography.demographics import Demographics
from champyons.core.domain.value_objects.geography.culture import Culture
from pathlib import Path
import json, random

DATA_DIR = Path(__file__).parent.parent / "data"

def get_demographics_by_code(*codes: str) -> Demographics:
    demographics_path = DATA_DIR / "demographics"

    # iterate all passed codes and return first json file that exists
    for code in codes:
        file_path = demographics_path / f"{code}.json"
        if not file_path.exists():
            continue
        return Demographics.from_json_file(code)

    # Fallback: default demographics (world), with default parameters
    return Demographics(code="world")
    
def get_culture_by_code(code: str) -> Culture:
    # TO-DO: include fallback when the culture json file does not exist.
    return Culture.from_json_file(code)

def generate_person(residence_code: str, rng: random.Random|None = None):
    rng = rng or random.Random()

    # TO-DO: residence nation will be chosen from a random city (weighted by population) of the nation. Other nationality will be chosen if available (nation otherwise)
    residence_nation = residence_code
    residence_demographics = get_demographics_by_code(residence_nation)
    if rng.random() > residence_demographics.immigrant_probability:
        # Nation of birth = Nation of residence
        nation_of_birth = residence_nation
        nation_of_birth_demographics = residence_demographics
    else:
        # Inmigrant from another nation
        nation_of_birth = rng.choices(list(residence_demographics.immigration_sources.keys()), weights=list(residence_demographics.immigration_sources.values()))[0]
        nation_of_birth_demographics = get_demographics_by_code(nation_of_birth)

    # TO-DO: city of birth is chosen from nation of birth
    cultures = nation_of_birth_demographics.cultures
    
    culture = rng.choices(list(cultures.keys()), weights=list(cultures.values()))[0]
    full_name = get_culture_by_code(culture).get_random_fullname("male") # TO-DO: common name and display name must be generated as well.

    # Nationalities. TO-DO: nationality is inherited from city's other nationality (via local region) and nationality.
    nationalities = set()
    if nation_of_birth_demographics.nationality_rules.nationality_by_birth:
        nationalities.add(nation_of_birth)
    
    if get_demographics_by_code(culture).nationality_rules.nationality_by_ancestry:
        nationalities.add(culture)

    # TO-DO. Random other nationalities could be added.


    person = {
        "name": " ".join(full_name),
        "residence": residence_nation,
        "nationalities": nationalities,
        "nation_of_birth": nation_of_birth,
        "culture": culture
    }

    return person

