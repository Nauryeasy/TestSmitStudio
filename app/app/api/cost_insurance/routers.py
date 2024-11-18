import datetime

from fastapi import APIRouter
from punq import Container

from app.app.api.cost_insurance.schemas import CargoSchemasRequest, CargoSchemasResponse, CargoSchemaResponse
from app.logic.container import get_container
from app.logic.mediator import QueryMediator
from app.logic.queryes.tariff.queryes import CalcCostInsuranceQuery, CargoDTO

router = APIRouter()


@router.post("/cost_insurance", response_model=CargoSchemasResponse)
async def create_tariffs(data: CargoSchemasRequest):
    container: Container = get_container()
    mediator: QueryMediator = container.resolve(QueryMediator)

    cargos = await mediator.handle_query(
        CalcCostInsuranceQuery(
            cargos=[
                CargoDTO(
                    declared_value=cargo.declared_value,
                    cargo_type=cargo.cargo_type,
                    date=datetime.datetime.strptime(cargo.date, "%Y-%m-%d").date()
                )
                for cargo in data.cargos
            ]
        )
    )

    return CargoSchemasResponse(cargos=[
        CargoSchemaResponse(
            declared_value=cargo.declared_value,
            cargo_type=cargo.cargo_type,
            date=str(cargo.date),
            cost_insurance=cargo.cost_insurance
        )
        for cargo in cargos
    ])
