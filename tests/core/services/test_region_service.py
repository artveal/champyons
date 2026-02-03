import pytest

from champyons.core.services.region_service import RegionService
from champyons.repositories.sqlalchemy.region_repository import SqlAlchemyRegionRepository
from champyons.schemas.region import RegionCreate, RegionUpdate

@pytest.fixture()
def region_service(db_session, translation_service):
    region_repo = SqlAlchemyRegionRepository(db=db_session)
    return RegionService(region_repo, translation_service)

def test_region_service_create(region_service: RegionService):
    data = RegionCreate(
        default_name="South Europe",
    )

    result = region_service.create(data)

    assert result.id is not None
    assert result.default_name == "South Europe"

def test_region_service_update(region_service: RegionService):
    created = region_service.create(
        RegionCreate(default_name="America")
    )

    update = RegionUpdate(
        default_name="North America",
    )

    updated = region_service.update(created.id, update)

    assert updated.id == created.id # both ids match as both objects refer to the same database entry
    assert updated.default_name == "North America"  # updated value
