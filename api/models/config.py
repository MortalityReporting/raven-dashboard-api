from sqlalchemy import JSON, String, MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    metadata_obj: MetaData = MetaData(schema="dashboard")
    pass

class Config(Base):
    __tablename__: str = 'configuration'
    env_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    json: Mapped[JSON] = mapped_column(JSON)
