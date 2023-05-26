from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_object_or_404(db: AsyncSession, model, condition):
    obj = await db.scalar(select(model).where(condition))
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{model.__name__} model instance not found')
    return obj


async def get_all_objects(db: AsyncSession, model):
    result = await db.scalars(select(model))
    return result.all()





