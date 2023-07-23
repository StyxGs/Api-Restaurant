from fastapi import HTTPException


async def not_found(result, detail):
    if not result:
        raise HTTPException(status_code=404, detail=detail)


async def exists():
    raise HTTPException(status_code=400, detail='submenu already exists')
