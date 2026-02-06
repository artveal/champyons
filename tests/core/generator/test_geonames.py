from champyons.core.adapters.geonames import geonames
import pytest

@pytest.fixture
def geonames_user() -> str:
    return "artveal"

def test_search_by_id(geonames_user):
    amsterdam = geonames.parse_from_geonames_id(username=geonames_user, geonames_id=2759794)
    assert amsterdam.alternateNames[0].lang == "ko"
    assert amsterdam.geonameId == 2759794

def test_search_by_name(geonames_user):
    noord_holland = geonames.parse_from_geonames_search(username=geonames_user, name_equals="Noord-Holland")
    assert noord_holland[0].geonameId == 2749879


def test_search_by_children(geonames_user):
    next_id = 6255148
    counter = 0
    while True:
        results = geonames.parse_children_from_geonames_id(username=geonames_user, geonames_id=next_id)
        if not results:
            break
        counter += 1
        next_id = results[0].geonameId
    assert counter > 0