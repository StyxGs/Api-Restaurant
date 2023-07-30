from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.core.models.dto.dish import DishDTO
from src.core.services.errors import exists, not_found
from src.infrastructure.db.dao.rbd.dish import DishDAO
from src.infrastructure.db.models import Dish


async def service_create_dish(menu_id: UUID, submenu_id: UUID, dto: DishDTO, dao: DishDAO) -> Dish:
    try:
        data: dict = dto.get_data
        data['submenu_id'] = submenu_id
        result: Dish = await dao.create(data, Dish)
        await dao.commit()
        return result
    except IntegrityError:
        await exists()


async def service_get_dishes(menu_id: UUID, submenu_id: UUID, dao: DishDAO) -> list[tuple]:
    result: list[tuple] | None = await dao.get_list(submenu_id)
    return result


async def service_get_dish(submenu_id: UUID, menu_id: UUID, dish_id: UUID, dao: DishDAO) -> tuple:
    result: tuple = await dao.get_one(submenu_id, dish_id)
    await not_found(result, 'dish not found')
    return result


async def service_update_dish(dto: DishDTO, menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: DishDAO) -> tuple:
    result: tuple = await dao.update(dto.get_data, submenu_id, dish_id)
    await not_found(result, 'dish not found')
    await dao.commit()
    dish: tuple = await dao.get_one(submenu_id, dish_id)
    return dish


async def service_delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: DishDAO) -> dict:
    result = await dao.delete(submenu_id, dish_id)
    await not_found(result, 'dish not found')
    await dao.commit()
    return {'status': True, 'message': 'The dish has been deleted'}
