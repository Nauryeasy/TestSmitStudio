from dataclasses import dataclass

from app.domain.events.tariff import DeleteTariffEvent, UpdateTariffEvent
from app.domain.tariff import Tariff
from app.infra.filters.tariff import TariffFilter
from app.infra.message_broker.producer.tariff import BaseTariffProducer
from app.infra.repositories.base import BaseTariffRepo
from app.logic.commands.base import BaseCommandHandler, CT, CR
from app.logic.commands.tariff.commands import AddTariffsCommand, DeleteTariffCommand, UpdateTariffCommand


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


@dataclass(frozen=True)
class DeleteTariffCommandHandler(BaseCommandHandler):
    tariff_repo: BaseTariffRepo

    async def handle(self, command: DeleteTariffCommand):
        entity = (await self.tariff_repo.select(filter=TariffFilter(oid=command.oid)))[0]
        entity = await self.tariff_repo.delete(entity)

        return entity


@dataclass(frozen=True)
class UpdateTariffCommandHandler(BaseCommandHandler):
    tariff_repo: BaseTariffRepo

    async def handle(self, command: UpdateTariffCommand):
        entity = Tariff(
            oid=command.oid,
            date=command.date,
            rate=command.rate,
            cargo_type=command.cargo_type
        )

        await self.tariff_repo.update(entity)

        return entity


@dataclass(frozen=True)
class ProduceDeleteTariffEvent(BaseCommandHandler):
    tariff_repo: BaseTariffRepo
    tariff_producer: BaseTariffProducer

    async def handle(self, command: DeleteTariffCommand) -> None:
        entity = (await self.tariff_repo.select(filter=TariffFilter(oid=command.oid)))[0]
        event = DeleteTariffEvent(
            entity=entity
        )

        self.tariff_producer.produce(event)


@dataclass(frozen=True)
class ProduceUpdateTariffEvent(BaseCommandHandler):
    tariff_repo: BaseTariffRepo
    tariff_producer: BaseTariffProducer

    async def handle(self, command: UpdateTariffCommand) -> None:
        entity = (await self.tariff_repo.select(filter=TariffFilter(oid=command.oid)))[0]
        event = UpdateTariffEvent(
            entity=entity,
            new_entity=Tariff(
                oid=command.oid,
                date=command.date,
                rate=command.rate,
                cargo_type=command.cargo_type
            )
        )

        self.tariff_producer.produce(event)
