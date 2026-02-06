from sqlalchemy import Table, Column, ForeignKey
from champyons.db.base import Base

nation_region_table = Table(
    "nation_region",
    Base.metadata,
    Column("nation_id", ForeignKey("nation.id"), ondelete="CASCADE", primary_key=True),
    Column("region_id", ForeignKey("region.id"), ondelete="CASCADE", primary_key=True),
)
