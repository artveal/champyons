from champyons.core.services.continent_service import ContinentService
from champyons.schemas.continent import ContinentCreate, ContinentUpdate
from champyons.core.services.translation_service import ReadModelTranslationService

def test_continent_service_create(continent_create_example: ContinentCreate, continent_service: ContinentService):
    result = continent_service.create(continent_create_example)

    assert result.id is not None
    assert result.code == "EU"
    assert result.default_name == "Europe"

def test_continent_service_update(continent_create_example: ContinentCreate, continent_service: ContinentService):
    created = continent_service.create(continent_create_example)

    update = ContinentUpdate(
        default_name="North America",
        code="NA"
    )

    updated = continent_service.update(created.id, update)

    assert updated.id == created.id # both ids match as both objects refer to the same database entry
    assert updated.default_name == "North America"  # updated value
    assert updated.code == "NA" # updated value 

def test_continent_service_partial_update(continent_create_example: ContinentCreate, continent_service: ContinentService):
    created = continent_service.create(continent_create_example)

    update = ContinentUpdate(default_name="Oceania")

    updated = continent_service.update(created.id, update)

    assert updated.default_name == "Oceania" # updated value
    assert updated.code == "EU" # unchanged value

def test_continent_creation_from_geonames(continent_service: ContinentService, read_model_translation_service: ReadModelTranslationService):
    for c in continent_service.create_all_from_geonames("artveal"):
        print(read_model_translation_service.translate(c))