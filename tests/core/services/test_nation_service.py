from champyons.core.services.nation_service import NationService
from champyons.schemas.nation import NationCreate, NationUpdate
from champyons.core.services.translation_service import ReadModelTranslationService

def test_nation_service_create(nation_create_example: NationCreate, nation_service: NationService):
    result = nation_service.create(nation_create_example)

    assert result.id is not None
    assert result.code == "IT"
    assert result.default_name == "Italy"

def test_nation_service_create_with_continent_and_region(nation_service: NationService, continent_create_example, continent_service):
    continent_service.create(continent_create_example)
    n_create = NationCreate(
        default_name="Spain",
        code="ES",
        continent_id=1
    )
    created = nation_service.create(n_create)

    assert created.continent
    assert created.continent.default_name == "Europe"


def test_nation_service_update(nation_create_example: NationCreate, nation_service: NationService):
    created = nation_service.create(nation_create_example)

    update = NationUpdate(
        default_name="France",
        active=False,
    )

    updated = nation_service.update(created.id, update)

    assert updated.id == created.id # both ids match as both objects refer to the same database entry
    assert updated.default_name == "France"  # updated value
    assert updated.active is False # updated value

def test_nation_service_partial_update(nation_create_example: NationCreate, nation_service: NationService):
    created = nation_service.create(nation_create_example)

    update = NationUpdate(default_name="Germany")
    updated = nation_service.update(created.id, update)

    assert updated.default_name == "Germany" # updated value
    assert updated.code == "IT" # unchanged value

def test_nation_translations_in_create_model(nation_create_example: NationCreate):   
    assert nation_create_example.name_translations[0].translation == "Italia"
    assert nation_create_example.name_translations[1].translation == "Italien"

def test_nation_translations_are_persisted(nation_create_example: NationCreate, nation_service: NationService):
    created = nation_service.create(nation_create_example)

    translations = nation_service.translation_service._repo.get_translations(
        keys={("nation", created.id)},
        lang="it",
    )

    assert translations, "No translations found in repository"
    assert "name" in translations[("nation", created.id)]
    assert translations[("nation", created.id)]["name"]["it"] == "Italia"
    assert translations[("nation", created.id)]["denonyms"]["it"][2] == "italiani"

def test_nation_service_create_with_translations(nation_create_example: NationCreate, nation_service: NationService, read_model_translation_service: ReadModelTranslationService):
    created = nation_service.create(nation_create_example)
    loaded = nation_service.get_by_id(created.id)

    translations = read_model_translation_service.get_translations_of_model(loaded, "it")
    assert translations["name"]["it"] == "Italia"

    translated = read_model_translation_service.translate(loaded, "it")
    assert translated.name == "Italia"
    assert translated.denonyms[2] == "italiani"

def test_nation_service_update_translations(nation_create_example: NationCreate, nation_service: NationService, read_model_translation_service: ReadModelTranslationService, continent_service, continent_create_example):
    continent_service.create(continent_create_example)
    created = nation_service.create(nation_create_example)

    update = NationUpdate(
        continent_id=1,
        translated_names=[{"language": "hu", "translation": "Olaszország"}],
        translated_denonyms=[
            {"language": "es_ES", "translation": "italiano"},
            {"language": "es_ES", "translation": "italiana"},
            {"language": "es_ES", "translation": "italianos"},
            {"language": "es_ES", "translation": "italianas"}
        ]
    )
    updated = nation_service.update(created.id, update)

    loaded = nation_service.get_by_id(created.id)
    translations = read_model_translation_service.get_translations_of_model(loaded, "hu")
    assert translations.get("name", {})["hu"] == "Olaszország"

    translated = read_model_translation_service.translate(loaded, "es_ES")

    assert translated.name == "Italy" # This translation should not be found, therefore default name should be returned
    assert translated.denonyms[2] == "italianos"
    assert translated.continent and translated.continent.name == "Europa"

def test_nation_service_from_geonames(nation_service: NationService, read_model_translation_service: ReadModelTranslationService):
    created = nation_service.create_from_geonames(2510769, "artveal")
    translated = read_model_translation_service.translate(created, "es_ES")
    assert translated.name == "España"
    assert translated.name_translations["en"] == "Spain"



    


    


    
