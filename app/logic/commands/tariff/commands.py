from dataclasses import dataclass
from datetime import datetime

from app.logic.commands.base import BaseCommand


@dataclass(frozen=True)
class AddTariffDTO:
    date: datetime.date
    rate: float
    cargo_type: str


@dataclass(frozen=True)
class AddTariffsCommand(BaseCommand):
    tariffs: list[AddTariffDTO]


@dataclass(frozen=True)
class DeleteTariffCommand(BaseCommand):
    oid: str


@dataclass(frozen=True)
class UpdateTariffCommand(BaseCommand):
    oid: str
    date: datetime.date
    rate: float
    cargo_type: str
