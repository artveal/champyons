from typing import List
from sqlalchemy.orm import Session, selectinload
from champyons.core.repositories.nation_region import NationRegionRepository
from champyons.db.models.nation import Nation
from champyons.db.models.region import Region
from champyons.db.models.nation_region import nation_region_table

class SQLAlchemyNationRegionRepository(NationRegionRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_nation_to_region(self, nation_id: int, region_id: int) -> None:
        exists = self.session.query(nation_region_table).filter_by(
            nation_id=nation_id,
            region_id=region_id
        ).first()
        if not exists:
            self.session.execute(
                nation_region_table.insert().values(
                    nation_id=nation_id,
                    region_id=region_id
                )
            )
            self.session.commit()

    def remove_nation_from_region(self, nation_id: int, region_id: int) -> None:
        self.session.execute(
            nation_region_table.delete().where(
                (nation_region_table.c.nation_id == nation_id) &
                (nation_region_table.c.region_id == region_id)
            )
        )
        self.session.commit()

    def get_regions_for_nation(self, nation_id: int) -> List[Region]:
        nation = self.session.query(Nation).options(
            selectinload(Nation.regions)
        ).filter(Nation.id == nation_id).one()
        return nation.regions

    def get_nations_for_region(self, region_id: int) -> List[Nation]:
        region = self.session.query(Region).options(
            selectinload(Region.nations)
        ).filter(Region.id == region_id).one()
        return region.nations
