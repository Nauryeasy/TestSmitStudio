from pydantic import BaseModel


class CargoSchema(BaseModel):
    declared_value: float
    cargo_type: str
    date: str


class CargoSchemasRequest(BaseModel):
    cargos: list[CargoSchema]


class CargoSchemaResponse(BaseModel):
    declared_value: float
    cargo_type: str
    date: str
    cost_insurance: float


class CargoSchemasResponse(BaseModel):
    cargos: list[CargoSchemaResponse]
