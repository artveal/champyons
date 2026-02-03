from datetime import datetime
from champyons.core.domain.entities.nation import Nation as NationEntity
from champyons.core.timezone import now_server


def test_nation_entity_creation():
    now = now_server()

    nation = NationEntity(
        id=1,
        code="ES",
        name="Spain",
        continent_id=1,
        region_id=None,
        parent_id=None,
        active=True,
        created_at=now,
        updated_at=now,
    )

    assert nation.id == 1
    assert nation.code == "ES"
    assert nation.name == "Spain"
    assert nation.active is True
    assert nation.created_at == now