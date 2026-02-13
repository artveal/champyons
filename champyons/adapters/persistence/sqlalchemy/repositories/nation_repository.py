from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Session
from champyons.adapters.persistence.sqlalchemy.models.country import Nation as NationModel
from champyons.core.domain.entities.geography.country import Nation as NationEntity
from champyons.core.ports.repositories.country import NationRepository

class SqlAlchemyNationRepository(NationRepository):
    """SQLAlchemy implementation of NationRepository."""
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, entity_id: int) -> NationEntity | None:
        stmt = sa.select(NationModel).filter(NationModel.id == entity_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result.to_entity(include_children=True) if result else None

    def get_all(self) -> List[NationEntity]:
        stmt = sa.select(NationModel)
        results = self.session.execute(stmt).scalars().all()
        return [n.to_entity(include_children=True) for n in results]

    def save(self, entity: NationEntity) -> NationEntity:
        if entity.id is None:
            # CREATE
            model = NationModel.from_entity(entity)
            self.session.add(model)
        else:
            # UPDATE
            model = self.session.get(NationModel, entity.id)
            if model is None:
                raise ValueError(f"Nation {entity.id} not found")

            model.update_from_entity(entity)

        self.session.commit()
        self.session.refresh(model)

        return model.to_entity(include_children=True)

    def delete(self, entity: NationEntity) -> None:
        stmt = sa.select(NationModel).filter(NationModel.id == entity.id)
        result = self.session.execute(stmt).scalar_one_or_none()
        if result:
            self.session.delete(result)
            self.session.commit()

    def get_by_code(self, code: str) -> NationEntity | None:
        stmt = sa.select(NationModel).filter(NationModel.code == code)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result.to_entity(include_children=True) if result else None

    def get_by_continent_id(self, continent_id: int) -> List[NationEntity]:
        stmt = sa.select(NationModel).filter(NationModel.continent_id == continent_id)
        results = self.session.execute(stmt).scalars().all()
        return [n.to_entity(include_children=True) for n in results]
