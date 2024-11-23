import datetime
from dataclasses import dataclass


@dataclass
class TariffFilter:
    oid: str | None = None
    date: datetime.date | None = None
    cargo_type: str | None = None
