import pytest
from sqlalchemy.orm import Session

from champyons.db.models.nation import Nation
from champyons.repositories.sqlalchemy.nation_repository import SqlAlchemyNationRepository

@pytest.fixture()
def nation_sqlalchemy_repo(db_session):
    return SqlAlchemyNationRepository(db_session)

def test_nation_repository_create_and_get(db_session: Session, nation_sqlalchemy_repo: SqlAlchemyNationRepository):
    nation = Nation(
        code="ES",
        default_name="Spain",
        active=True,
    )

    db_session.add(nation)
    db_session.commit()

    fetched = nation_sqlalchemy_repo.get_by_id(nation.id)

    assert fetched is not None
    assert fetched.code == "ES"
    assert fetched.name == "Spain"