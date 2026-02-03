import pytest
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker

from champyons.db.base import Base

from champyons.core.services.nation_service import NationService, NationCreate
from champyons.core.services.continent_service import ContinentService, ContinentCreate
from champyons.core.services.translation_service import ReadModelTranslationService, TranslationService

from champyons.repositories.sqlalchemy.nation_repository import SqlAlchemyNationRepository
from champyons.repositories.sqlalchemy.continent_repository import SqlAlchemyContinentRepository
from champyons.repositories.sqlalchemy.translation_repostory import SqlAlchemyTranslationRepository

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine("sqlite:///:memory:")

    # Activar PRAGMA foreign_keys para SQLite
    @event.listens_for(engine, "connect")
    def enable_sqlite_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Crear todas las tablas
    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(db_engine: Engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

"""
SERVICES
"""



@pytest.fixture(scope="function")
def nation_service(db_session, translation_service):
    nation_repo = SqlAlchemyNationRepository(db=db_session)
    continent_repo = SqlAlchemyContinentRepository(db=db_session)
    return NationService(nation_repo, continent_repo, translation_service)

@pytest.fixture(scope="module")
def nation_create_example():
    return NationCreate(
        code="IT",
        default_name="Italy",
        translated_names=[
            {"language": "it", "translation": "Italia"},
            {"language": "de", "translation": "Italien"}
        ],
        translated_denonyms=[
            {"language": "it", "translation": "italiano"},
            {"language": "it", "translation": "italiana"},
            {"language": "it", "translation": "italiani"},
            {"language": "it", "translation": "italiane"},
        ]
    )

@pytest.fixture(scope="function")
def continent_service(db_session, translation_service):
    continent_repo = SqlAlchemyContinentRepository(db=db_session)
    return ContinentService(continent_repo, translation_service)

@pytest.fixture(scope="module")
def continent_create_example():
    return ContinentCreate(
        default_name="Europe",
        code="EU",
        translated_names=[
            {"language": "it", "translation": "Europa"},
            {"language": "es", "translation": "Europa"},
        ]
    )

@pytest.fixture(scope="function")
def read_model_translation_service(db_session):
    translation_repo = SqlAlchemyTranslationRepository(db=db_session)
    return ReadModelTranslationService(translation_repo)

@pytest.fixture(scope="function")
def translation_service(db_session):
    translation_repo = SqlAlchemyTranslationRepository(db=db_session)
    return TranslationService(translation_repo)


