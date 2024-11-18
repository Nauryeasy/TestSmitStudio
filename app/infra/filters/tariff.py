import datetime
from dataclasses import dataclass


@dataclass
class TariffFilter:
    date: datetime.date
    cargo_type: str
