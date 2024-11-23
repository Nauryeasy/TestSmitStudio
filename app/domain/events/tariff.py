from dataclasses import dataclass

from app.domain.events.base import BaseEvent
from app.domain.tariff import Tariff


@dataclass(frozen=True)
class UpdateTariffEvent(BaseEvent):
    entity: Tariff
    new_entity: Tariff


@dataclass(frozen=True)
class DeleteTariffEvent(BaseEvent):
    entity: Tariff
