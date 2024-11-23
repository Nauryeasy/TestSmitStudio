from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.events.base import BaseEvent


@dataclass
class BaseEventConverter(ABC):

    @abstractmethod
    def convert_event_to_message(self, event: BaseEvent) -> dict:
        ...

    @abstractmethod
    def convert_message_to_event(self, message: dict) -> BaseEvent:
        ...
