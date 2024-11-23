import datetime
from typing import Dict, List
from pydantic import BaseModel, Field, RootModel

from app.domain.tariff import Tariff


class TariffSchema(BaseModel):
    cargo_type: str = Field(..., example="Glass")
    rate: float = Field(..., example=0.04)


class TariffSchemasRequest(RootModel):
    root: Dict[str, List[TariffSchema]]

    class Config:
        schema_extra = {
            "example": {
                "2020-06-01": [
                    {"cargo_type": "Glass", "rate": 0.04},
                    {"cargo_type": "Other", "rate": 0.01}
                ],
                "2020-07-01": [
                    {"cargo_type": "Glass", "rate": 0.035},
                    {"cargo_type": "Other", "rate": 0.015}
                ]
            }
        }


class UpdateTariffSchema(BaseModel):
    date: datetime.date = Field(default=None, example="2020-06-01")
    rate: float = Field(default=None, example=0.04)
    cargo_type: str = Field(default=None, example="Glass")


class TariffSchemaResponse(BaseModel):
    oid: str
    date: datetime.date
    rate: float
    cargo_type: str

    @staticmethod
    def from_entity(entity: Tariff):
        return TariffSchemaResponse(
            oid=entity.oid,
            date=entity.date,
            rate=entity.rate,
            cargo_type=entity.cargo_type
        )


class ListTariffSchemaResponse(BaseModel):
    tariffs: List[TariffSchemaResponse]

    @staticmethod
    def from_entities(entities: List[Tariff]):
        return ListTariffSchemaResponse(
            tariffs=[TariffSchemaResponse.from_entity(entity) for entity in entities]
        )
