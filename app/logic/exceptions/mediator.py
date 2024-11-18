from dataclasses import dataclass
from typing import Type

from app.logic.commands.base import CT
from app.logic.events.base import ET
from app.logic.queryes.base import QT


@dataclass(eq=False)
class EventHandlerNotRegisteredException(Exception):

    event_class: Type[ET]

    @property
    def message(self):
        return f'Event handler for {self.event_class} is not registered'

    def __str__(self):
        return self.message


@dataclass(eq=False)
class CommandHandlerNotRegisteredException(Exception):

    command_class: Type[CT]

    @property
    def message(self):
        return f'Command handler for {self.command_class} is not registered'

    def __str__(self):
        return self.message


@dataclass(eq=False)
class QueryHandlerNotRegisteredException(Exception):

    query_class: Type[QT]

    @property
    def message(self):
        return f'Query handler for {self.query_class} is not registered'

    def __str__(self):
        return self.message
