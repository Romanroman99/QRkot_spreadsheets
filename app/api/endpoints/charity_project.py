from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_already_invested,
    check_exist,
    check_invested_sum,
    check_name_duplicate,
    check_project_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investing import investing

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создает новый благотворительный проект.
    """
    await check_name_duplicate(project.name, session)
    await charity_project_crud.get_project_id_by_name(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await investing(new_project, Donation, session)
    return new_project


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список всех благотворительных проектов.
    """
    return await charity_project_crud.get_multi(session)


@router.patch(
    "/{id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Частично обновляет информацию о благотворительном проекте.
    """
    patch_project = await check_exist(id, session)
    check_project_closed(patch_project)
    if update_data.name is not None:
        await check_name_duplicate(update_data.name, session)
    if update_data.full_amount is not None:
        check_invested_sum(patch_project, update_data.full_amount)

    return await charity_project_crud.update(patch_project, update_data, session)


@router.delete(
    "/{id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Удаляет благотворительный проект.
    """
    project = await check_exist(id, session)
    check_already_invested(project)
    return await charity_project_crud.remove(project, session)
