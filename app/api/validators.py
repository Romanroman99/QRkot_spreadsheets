from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_exist(
    id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Сбор не найден!"
        )
    return project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


def check_invested_sum(project: CharityProject, new_amount: int):
    if project.invested_amount > new_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя установить сумму, ниже уже вложенной!",
        )
    return HTTPStatus.OK


def check_already_invested(charity_project: CharityProject):
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


def check_project_closed(charity_project: CharityProject):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )
