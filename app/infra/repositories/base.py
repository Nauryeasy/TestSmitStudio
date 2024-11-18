from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from app.domain.base import BaseEntity
from app.domain.tariff import Tariff
from app.infra.filters.base import BaseFilter
from app.infra.filters.tariff import TariffFilter
from app.infra.models.base_model import Base
from app.infra.models.tariff import TariffModel

T = TypeVar('T', bound=BaseEntity)
F = TypeVar('F', bound=BaseFilter)
M = TypeVar('M', bound=Base)


class BaseRepo(ABC, Generic[T, M, F]):

    @abstractmethod
    async def _model_to_entity(self, model: M) -> T:
        ...

    @abstractmethod
    async def _entity_to_model(self, entity: T) -> M:
        ...

    @abstractmethod
    async def insert(self, entity: T) -> None:
        ...

    @abstractmethod
    async def select(self, filter: F | None = None) -> list[T]:
        ...


class BaseTariffRepo(BaseRepo[Tariff, TariffModel, TariffFilter], ABC):
    ...
