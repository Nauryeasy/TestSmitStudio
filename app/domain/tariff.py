from dataclasses import dataclass
from datetime import datetime

from app.domain.base import BaseEntity
from app.domain.cargo import Cargo


@dataclass(eq=False)
class Tariff(BaseEntity):
    date: datetime.date
    rate: float
    cargo_type: str

    def calc_cost_insurance(self, cargo: Cargo) -> float:
        return cargo.declared_value * self.rate
