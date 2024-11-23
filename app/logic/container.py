from functools import lru_cache

import punq

from app.domain.events.tariff import UpdateTariffEvent, DeleteTariffEvent
from app.infra.message_broker.converters.tariff.convert_methods import convert_update_tariff_event_to_message, \
    convert_delete_tariff_event_to_message
from app.infra.message_broker.converters.tariff.tariff_converter import TariffEventConverter
from app.infra.message_broker.producer.tariff import KafkaTariffProducer, BaseTariffProducer
from app.infra.repositories.base import BaseTariffRepo
from app.infra.repositories.tariff import TariffRepo
from app.logic.commands.tariff.commands import AddTariffsCommand, DeleteTariffCommand, UpdateTariffCommand
from app.logic.commands.tariff.handlers import AddTariffsCommandHandler, DeleteTariffCommandHandler, \
    UpdateTariffCommandHandler, ProduceUpdateTariffEvent, ProduceDeleteTariffEvent
from app.logic.mediator import CommandMediator, QueryMediator
from app.configs import Settings
from app.infra.database import Database
from app.logic.queryes.tariff.handlers import CalcCostInsuranceQueryHandler, GetTariffsQueryHandler
from app.logic.queryes.tariff.queryes import CalcCostInsuranceQuery, GetTariffsQuery


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()
    container.register(punq.Container, instance=container)

    container.register(AddTariffsCommandHandler)
    container.register(DeleteTariffCommandHandler)
    container.register(UpdateTariffCommandHandler)
    container.register(ProduceUpdateTariffEvent)
    container.register(ProduceDeleteTariffEvent)

    container.register(CalcCostInsuranceQueryHandler)
    container.register(GetTariffsQueryHandler)

    container.register(Settings, instance=Settings(), scope=punq.Scope.singleton)

    def init_tariff_converter() -> TariffEventConverter:
        converter = TariffEventConverter()
        converter.register_event(UpdateTariffEvent, convert_update_tariff_event_to_message)
        converter.register_event(DeleteTariffEvent, convert_delete_tariff_event_to_message)

        return converter

    def init_command_mediator() -> CommandMediator:
        mediator = CommandMediator()

        mediator.register_command(AddTariffsCommand, container.resolve(AddTariffsCommandHandler))
        mediator.register_command(DeleteTariffCommand, container.resolve(DeleteTariffCommandHandler))
        mediator.register_command(UpdateTariffCommand, container.resolve(UpdateTariffCommandHandler))

        mediator.register_command(DeleteTariffCommand, container.resolve(ProduceDeleteTariffEvent))
        mediator.register_command(UpdateTariffCommand, container.resolve(ProduceUpdateTariffEvent))

        return mediator

    def init_query_mediator() -> QueryMediator:
        mediator = QueryMediator()

        mediator.register_query(CalcCostInsuranceQuery, container.resolve(CalcCostInsuranceQueryHandler))
        mediator.register_query(GetTariffsQuery, container.resolve(GetTariffsQueryHandler))

        return mediator

    container.register(
        Database,
        scope=punq.Scope.singleton,
        factory=lambda: Database(
            url=Settings().POSTGRES_URL,
            ro_url=Settings().POSTGRES_URL
        )
    )

    container.register(BaseTariffRepo, TariffRepo, scope=punq.Scope.singleton)

    container.register(CommandMediator, factory=init_command_mediator, scope=punq.Scope.singleton)
    container.register(QueryMediator, factory=init_query_mediator, scope=punq.Scope.singleton)

    container.register(TariffEventConverter, factory=init_tariff_converter, scope=punq.Scope.singleton)

    container.register(BaseTariffProducer, KafkaTariffProducer, scope=punq.Scope.singleton)

    return container


