from dataclasses import dataclass

from app.domain.cargo import Cargo
from app.infra.filters.tariff import TariffFilter
from app.infra.repositories.base import BaseTariffRepo
from app.logic.queryes.base import BaseQueryHandler
from app.logic.queryes.tariff.queryes import CalcCostInsuranceQuery


@dataclass(frozen=True)
class CalcCostInsuranceQueryHandler(BaseQueryHandler):
    tariff_repo: BaseTariffRepo

    async def handle(self, query: CalcCostInsuranceQuery) -> list[Cargo]:

        cargos = []

        for cargo in query.cargos:
            tariff = (await self.tariff_repo.select(
                filter=TariffFilter(date=cargo.date, cargo_type=cargo.cargo_type)
            ))[0]
            if not tariff:
                continue

            cargo_entity = Cargo(
                declared_value=cargo.declared_value,
                date=cargo.date,
                cargo_type=cargo.cargo_type
            )
            cargo_entity.cost_insurance = tariff.calc_cost_insurance(cargo_entity)

            cargos.append(cargo_entity)

        return cargos
