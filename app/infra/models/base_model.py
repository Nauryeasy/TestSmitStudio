from datetime import datetime, timezone
import re
from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    __table_args__ = {'extend_existing': True}
    
    oid = Column(String, primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__

        if name.endswith("Model"):
            name = name[:-5]

        pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
        name_snake_case = pattern.sub('_', name).lower()

        return name_snake_case
    