import datetime

from fastapi import APIRouter
from punq import Container

from app.app.api.tariff.schemas import TariffSchemasRequest
from app.logic.commands.tariff.commands import AddTariffsCommand, AddTariffDTO
from app.logic.container import get_container
from app.logic.mediator import CommandMediator

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
