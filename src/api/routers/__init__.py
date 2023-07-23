from fastapi import APIRouter

from src.api.routers import menu


def setup(router: APIRouter):
    menu.setup(router)
