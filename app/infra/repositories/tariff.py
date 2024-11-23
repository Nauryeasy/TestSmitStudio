from dataclasses import dataclass

from punq import Container

from sqlalchemy import select, delete

from app.domain.tariff import Tariff
from app.infra.database import Database
from app.infra.filters.tariff import TariffFilter
from app.infra.models.tariff import TariffModel
from app.infra.repositories.base import BaseTariffRepo, F, T, M


@dataclass
class TariffRepo(BaseTariffRepo):

    database: Database
    container: Container

    async def _model_to_entity(self, model: TariffModel) -> Tariff:
        return Tariff(
            oid=model.oid,
            date=model.date,
            rate=model.rate,
            cargo_type=model.cargo_type
        )

    async def _entity_to_model(self, entity: Tariff) -> TariffModel:
        return TariffModel(
            oid=entity.oid,
            date=entity.date,
            rate=entity.rate,
            cargo_type=entity.cargo_type
        )

    def _make_query(self, filter: TariffFilter | None = None):
        query = select(TariffModel)
        if filter:
            if filter.date:
                query = query.where(TariffModel.date == filter.date)
            if filter.cargo_type:
                query = query.where(TariffModel.cargo_type == filter.cargo_type)

        return query

    async def insert(self, entity: Tariff) -> None:
        async with self.database.get_session() as session:
            try:
                session.add(await self._entity_to_model(entity))
            except Exception as e:
                raise ValueError(f"Exception: {e}")

    async def select(self, filter: TariffFilter | None = None) -> list[Tariff]:
        async with self.database.get_session() as session:
            query = self._make_query(filter)
            result = await session.scalars(query)
            return [await self._model_to_entity(item) for item in result]

    async def update(self, entity: Tariff):
        async with self.database.get_session() as session:
            await session.merge(await self._entity_to_model(entity))
        return entity

    async def delete(self, entity: Tariff):
        async with self.database.get_session() as session:
            await session.execute(delete(TariffModel).where(TariffModel.oid == entity.oid))
        return entity
