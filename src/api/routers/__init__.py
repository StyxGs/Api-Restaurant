from fastapi import APIRouter

from src.api.routers import dish, menu, submenu


def setup() -> APIRouter:
    router = APIRouter(prefix='/api/v1')
    menu.setup(router)
    submenu.setup(router)
    dish.setup(router)
    return router
