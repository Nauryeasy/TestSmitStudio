from dataclasses import dataclass

from app.domain.tariff import Tariff
from app.infra.repositories.base import BaseTariffRepo
from app.logic.commands.base import BaseCommandHandler
from app.logic.commands.tariff.commands import AddTariffsCommand


@dataclass(frozen=True)
class AddTariffsCommandHandler(BaseCommandHandler):
    tariff_repo: BaseTariffRepo

    async def handle(self, command: AddTariffsCommand):
        for tariff in command.tariffs:

            entity = Tariff(
                date=tariff.date,
                rate=tariff.rate,
                cargo_type=tariff.cargo_type
            )

            await self.tariff_repo.insert(entity)
