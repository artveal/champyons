import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

from champyons.db.base import Base

@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")

    # Activar PRAGMA foreign_keys para SQLite
    @event.listens_for(engine, "connect")
    def enable_sqlite_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Crear todas las tablas
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()