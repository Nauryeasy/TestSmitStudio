from functools import lru_cache

import punq

from app.infra.repositories.base import BaseTariffRepo
from app.infra.repositories.tariff import TariffRepo
from app.logic.commands.tariff.commands import AddTariffsCommand
from app.logic.commands.tariff.handlers import AddTariffsCommandHandler
from app.logic.mediator import CommandMediator, QueryMediator
from app.configs import Settings
from app.infra.database import Database
from app.logic.queryes.tariff.handlers import CalcCostInsuranceQueryHandler
from app.logic.queryes.tariff.queryes import CalcCostInsuranceQuery


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()
    container.register(punq.Container, instance=container)

    container.register(AddTariffsCommandHandler)

    container.register(CalcCostInsuranceQueryHandler)

    container.register(Settings, instance=Settings(), scope=punq.Scope.singleton)

    def init_command_mediator() -> CommandMediator:
        mediator = CommandMediator()

        mediator.register_command(AddTariffsCommand, container.resolve(AddTariffsCommandHandler))

        return mediator

    def init_query_mediator() -> QueryMediator:
        mediator = QueryMediator()

        mediator.register_query(CalcCostInsuranceQuery, container.resolve(CalcCostInsuranceQueryHandler))

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

    return container


