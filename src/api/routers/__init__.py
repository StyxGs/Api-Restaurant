from fastapi import APIRouter

from src.api.routers import menu, submenu


def setup() -> APIRouter:
    router = APIRouter(prefix='/api/v1')
    menu.setup(router)
    submenu.setup(router)
    return router
