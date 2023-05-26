from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_object_or_404(db: AsyncSession, model, condition, *args):
    obj = await db.scalar(select(model).where(condition))
    if obj is None:
        message = f'{model.__name__} model instance not found.'
        if args:
            message += f'Invalid input data: {args}'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message)
    return obj


async def get_all_objects(db: AsyncSession, model):
    result = await db.scalars(select(model))
    return result.all()
