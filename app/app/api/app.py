from fastapi import FastAPI

from app.app.api.tariff.routers import router as tariff_router
from app.app.api.cost_insurance.routers import router as cost_insurance_router
from app.logic.container import get_container
from app.configs import Settings


def create_app() -> FastAPI:

    settings: Settings = get_container().resolve(Settings)

    app = FastAPI(
        title='Smit API',
        root_path='/api',
        docs_url='/docs',
        debug=True,
    )

    app.include_router(tariff_router)
    app.include_router(cost_insurance_router)

    return app
