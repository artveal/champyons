from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Session
from champyons.adapters.persistence.sqlalchemy.models.nation import Nation as NationModel
from champyons.core.domain.entities.geography.nation import Nation as NationEntity
from champyons.core.ports.repositories.nation import NationRepository

class SqlAlchemyNationRepository(NationRepository):
    """SQLAlchemy implementation of NationRepository."""
    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, entity_id: int) -> NationEntity | None:
        stmt = sa.select(NationModel).filter(NationModel.id == entity_id)
        result = self._db.execute(stmt).scalar_one_or_none()
        return result.to_entity(include_children=True) if result else None

    def get_all(self) -> List[NationEntity]:
        stmt = sa.select(NationModel)
        results = self._db.execute(stmt).scalars().all()
        return [n.to_entity(include_children=True) for n in results]

    def save(self, entity: NationEntity) -> NationEntity:
        if entity.id is None:
            # CREATE
            model = NationModel.from_entity(entity)
            self._db.add(model)
        else:
            # UPDATE
            model = self._db.get(NationModel, entity.id)
            if model is None:
                raise ValueError(f"Nation {entity.id} not found")

            model.update_from_entity(entity)

        self._db.commit()
        self._db.refresh(model)

        return model.to_entity(include_children=True)

    def delete(self, entity: NationEntity) -> None:
        stmt = sa.select(NationModel).filter(NationModel.id == entity.id)
        result = self._db.execute(stmt).scalar_one_or_none()
        if result:
            self._db.delete(result)
            self._db.commit()

    def get_by_code(self, code: str) -> NationEntity | None:
        stmt = sa.select(NationModel).filter(NationModel.code == code)
        result = self._db.execute(stmt).scalar_one_or_none()
        return result.to_entity(include_children=True) if result else None

    def get_by_continent_id(self, continent_id: int) -> List[NationEntity]:
        stmt = sa.select(NationModel).filter(NationModel.continent_id == continent_id)
        results = self._db.execute(stmt).scalars().all()
        return [n.to_entity(include_children=True) for n in results]
