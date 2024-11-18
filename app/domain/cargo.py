import datetime
from dataclasses import dataclass

from app.domain.base import BaseEntity


@dataclass(eq=False)
class Cargo(BaseEntity):
    cargo_type: str
    date: datetime.date
    declared_value: float
    cost_insurance: float | None = None
