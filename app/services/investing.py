from datetime import datetime as dt
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AbstractBase, CharityProject, Donation


async def check_unfull_project(
    db_model: AbstractBase,  # модель из бд Donation(при создании проекта) или CreateProject(При донате)
    session: AsyncSession
) -> List[AsyncSession]:
    """
    1. Смотрит, есть ли не инвестированные свободные средства
    2. Есть ли проекты, нуждающиеся в инвестировании
    """
    unfully_invested = await session.execute(
        select(db_model).where(
            db_model.fully_invested == 0
        ).order_by(db_model.create_date)
    )
    unfully_invested = unfully_invested.scalars().all()
    return unfully_invested


async def investing(
    obj_in: AbstractBase,  # проект/донат (создание)
    db_model: AbstractBase,  # модель из бд Donation(при создании проекта) или CreateProject(При донате)
    session: AsyncSession
) -> AbstractBase:
    unfully_invested = await check_unfull_project(db_model, session)

    for model in unfully_invested:
        obj_in, model = await distribution(obj_in, model)
        session.add(model)
        session.add(obj_in)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def distribution(
    obj_in: AbstractBase,
    db_model: AbstractBase,
) -> List[AbstractBase]:
    rest_in = obj_in.full_amount - obj_in.invested_amount
    rest_model = db_model.full_amount - db_model.invested_amount

    if rest_in > rest_model:
        obj_in.invested_amount += rest_model
        await close_obj(db_model)
    elif rest_in < rest_model:
        db_model.invested_amount += rest_in
        await close_obj(obj_in)
    else:
        await close_obj(obj_in)
        await close_obj(db_model)

    return obj_in, db_model


async def close_obj(obj: Union[CharityProject, Donation]):
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = dt.now()
    return obj
