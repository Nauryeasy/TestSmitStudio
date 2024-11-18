from typing import Dict, List
from pydantic import BaseModel, Field, RootModel


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
