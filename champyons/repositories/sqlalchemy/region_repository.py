from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Session
from champyons.db.models.region import Region as RegionModel
from champyons.core.domain.entities.region import Region as RegionEntity
from champyons.core.repositories.region import RegionRepository

class SqlAlchemyRegionRepository(RegionRepository):
    """SQLAlchemy implementation of RegionRepository."""
    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, entity_id: int) -> RegionEntity | None:
        stmt = sa.select(RegionModel).filter(RegionModel.id == entity_id)
        result = self._db.execute(stmt).scalar_one_or_none()
        return result.to_entity(include_nations=True) if result else None

    def get_all(self) -> List[RegionEntity]:
        stmt = sa.select(RegionModel)
        results = self._db.execute(stmt).scalars().all()
        return [n.to_entity(include_nations=True) for n in results]

    def save(self, entity: RegionEntity) -> RegionEntity:
        if entity.id is None:
            # CREATE
            model = RegionModel.from_entity(entity)
            self._db.add(model)
        else:
            # UPDATE
            model = self._db.get(RegionModel, entity.id)
            if model is None:
                raise ValueError(f"Continent {entity.id} not found")

            model.update_from_entity(entity)

        self._db.commit()
        self._db.refresh(model)

        return model.to_entity(include_nations=True)

    def delete(self, entity: RegionEntity) -> None:
        stmt = sa.select(RegionModel).filter(RegionModel.id == entity.id)
        result = self._db.execute(stmt).scalar_one_or_none()
        if result:
            self._db.delete(result)
            self._db.commit()

