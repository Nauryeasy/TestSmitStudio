from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.events.base import BaseEvent


@dataclass
class BaseProducer(ABC):

    @abstractmethod
    def produce(self, event: BaseEvent) -> None:
        ...
