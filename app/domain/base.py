from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(eq=False)
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        kw_only=True,
    )

    def __eq__(self, value: 'BaseEntity') -> bool:
        return self.oid == value.oid
    
    def __hash__(self) -> int:
        return hash(self.oid)
