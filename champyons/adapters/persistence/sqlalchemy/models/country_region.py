from sqlalchemy import Table, Column, ForeignKey
from champyons.adapters.persistence.sqlalchemy.base import Base

country_region_table = Table(
    "country_region",
    Base.metadata,
    Column("country_id", ForeignKey("country.id"), ondelete="CASCADE", primary_key=True),
    Column("region_id", ForeignKey("region.id"), ondelete="CASCADE", primary_key=True),
)
