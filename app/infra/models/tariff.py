from sqlalchemy import Column, Float, String, Date

from app.infra.models.base_model import Base


class TariffModel(Base):
    date = Column(Date)
    rate = Column(Float)
    cargo_type = Column(String)
