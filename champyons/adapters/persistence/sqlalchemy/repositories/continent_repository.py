from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Session
from champyons.adapters.persistence.sqlalchemy.models.continent import Continent as ContinentModel
from champyons.core.domain.entities.geography.continent import Continent as ContinentEntity
from champyons.core.ports.repositories.continent import ContinentRepository

class SqlAlchemyContinentRepository(ContinentRepository):
    """SQLAlchemy implementation of ContinentRepository."""
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, entity_id: int) -> ContinentEntity | None:
        stmt = sa.select(ContinentModel).filter(ContinentModel.id == entity_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result.to_entity(include_nations=True) if result else None
    
    def get_by_code(self, code: str) -> ContinentEntity | None:
        stmt = sa.select(ContinentModel).filter(ContinentModel.code == code)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result.to_entity(include_nations=True) if result else None

    def get_all(self) -> List[ContinentEntity]:
        stmt = sa.select(ContinentModel)
        results = self.session.execute(stmt).scalars().all()
        return [n.to_entity(include_nations=True) for n in results]

    def save(self, entity: ContinentEntity) -> ContinentEntity:
        if entity.id is None:
            # CREATE
            model = ContinentModel.from_entity(entity)
            self.session.add(model)
        else:
            # UPDATE
            model = self.session.get(ContinentModel, entity.id)
            if model is None:
                raise ValueError(f"Continent {entity.id} not found")

            model.update_from_entity(entity)

        self.session.commit()
        self.session.refresh(model)

        return model.to_entity(include_nations=True)

    def delete(self, entity: ContinentEntity) -> None:
        stmt = sa.select(ContinentModel).filter(ContinentModel.id == entity.id)
        result = self.session.execute(stmt).scalar_one_or_none()
        if result:
            self.session.delete(result)
            self.session.commit()

