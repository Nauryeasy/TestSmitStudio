from dataclasses import dataclass
from datetime import datetime

from app.logic.queryes.base import BaseQuery


@dataclass(frozen=True)
class CargoDTO:
    declared_value: float
    date: datetime.date
    cargo_type: str


@dataclass(frozen=True)
class CalcCostInsuranceQuery(BaseQuery):
    cargos: list[CargoDTO]


@dataclass(frozen=True)
class GetTariffsQuery(BaseQuery):
    oid: str
    date: datetime.date
    cargo_type: str
