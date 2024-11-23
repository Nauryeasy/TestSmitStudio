import datetime

from fastapi import APIRouter
from punq import Container

from app.app.api.tariff.schemas import TariffSchemasRequest, TariffSchemaResponse, \
    ListTariffSchemaResponse, UpdateTariffSchema
from app.logic.commands.tariff.commands import AddTariffsCommand, AddTariffDTO, DeleteTariffCommand, UpdateTariffCommand
from app.logic.container import get_container
from app.logic.mediator import CommandMediator, QueryMediator
from app.logic.queryes.tariff.queryes import GetTariffsQuery

router = APIRouter()


@router.post("/tariff")
async def create_tariffs(data: TariffSchemasRequest):
    container: Container = get_container()
    mediator: CommandMediator = container.resolve(CommandMediator)

    tariffs = []
    for date_str, rates in data.root.items():
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        for rate in rates:
            tariffs.append(AddTariffDTO(
                date=date,
                rate=rate.rate,
                cargo_type=rate.cargo_type
            ))

    _ = await mediator.handle_command(
        AddTariffsCommand(
            tariffs=tariffs
        )
    )

    return {"message": "Tariffs created"}


@router.get("/tariff", response_model=ListTariffSchemaResponse)
async def get_tariffs(oid: str | None = None, date: datetime.date | None = None, cargo_type: str | None = None):
    container: Container = get_container()
    mediator: QueryMediator = container.resolve(QueryMediator)

    tariffs = await mediator.handle_query(
        GetTariffsQuery(
            oid=oid,
            date=date,
            cargo_type=cargo_type
        )
    )

    return ListTariffSchemaResponse.from_entities(tariffs)


@router.delete("/tariff/{tariff_oid}", response_model=TariffSchemaResponse)
async def delete_tariff(tariff_oid: str):
    container: Container = get_container()
    mediator: CommandMediator = container.resolve(CommandMediator)

    tariff, *_ = await mediator.handle_command(
        DeleteTariffCommand(
            oid=tariff_oid
        )
    )

    return TariffSchemaResponse.from_entity(tariff)


@router.patch("/tariff/{tariff_oid}", response_model=TariffSchemaResponse)
async def update_tariff(tariff_oid: str, data: UpdateTariffSchema):
    container: Container = get_container()
    mediator: CommandMediator = container.resolve(CommandMediator)

    tariff, *_ = await mediator.handle_command(
        UpdateTariffCommand(
            oid=tariff_oid,
            date=data.date,
            rate=data.rate,
            cargo_type=data.cargo_type
        )
    )

    return TariffSchemaResponse.from_entity(tariff)
