from collections import defaultdict
from dataclasses import dataclass, field
from typing import Type, Iterable

from app.logic.commands.base import CT, BaseCommandHandler, CR
from app.domain.events.base import ET, BaseEventHandler, ER
from app.logic.exceptions.mediator import EventHandlerNotRegisteredException, CommandHandlerNotRegisteredException, \
    QueryHandlerNotRegisteredException
from app.logic.queryes.base import QT, BaseQueryHandler, QR


@dataclass(eq=False)
class CommandMediator:
    events_map: dict[Type[ET], list[BaseEventHandler[ET, ER]]] = field(
        default_factory=lambda: defaultdict[Type[ET], list[BaseEventHandler[ET, ER]]](list),
        kw_only=True,
    )

    commands_map: dict[Type[CT], list[BaseCommandHandler[CT, CR]]] = field(
        default_factory=lambda: defaultdict[Type[CT], list[BaseCommandHandler[CT, CR]]](list),
        kw_only=True,
    )

    def register_event(self, event_type: Type[ET], handler: BaseEventHandler):
        self.events_map[event_type].append(handler)

    def register_command(self, command_type: Type[CT], handler: BaseCommandHandler):
        self.commands_map[command_type].append(handler)

    async def handle_event(self, event: ET) -> Iterable[ER]:

        event_type = event.__class__
        handlers = self.events_map[event_type]

        if not handlers:
            raise EventHandlerNotRegisteredException(event_type)

        return [await handler.handle(event) for handler in handlers]

    async def handle_command(self, command: CT) -> Iterable[CR]:

        command_type = command.__class__
        handlers = self.commands_map[command_type]

        if not handlers:
            raise CommandHandlerNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]


@dataclass(eq=False)
class QueryMediator:
    queries_map: dict[Type[QT], list[BaseQueryHandler[QT, QR]]] = field(
        default_factory=lambda: defaultdict[Type[QT], list[BaseQueryHandler[QT, QR]]](list),
        kw_only=True,
    )

    def register_query(self, query_type: Type[QT], handler: BaseQueryHandler):
        self.queries_map[query_type].append(handler)

    async def handle_query(self, query: QT) -> QR:
        query_type = query.__class__
        handlers = self.queries_map[query_type]

        if not handlers:
            raise QueryHandlerNotRegisteredException(query_type)

        return await handlers[0].handle(query)
