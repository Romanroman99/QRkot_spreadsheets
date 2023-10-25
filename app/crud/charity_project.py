from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        '''
        Получает идентификатор проекта по его имени.
        '''
        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == project_name)
        )
        return db_project_id.scalars().first()

    async def get_project_by_id(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        '''
        Получает проект по его идентификатору.
        '''
        db_project = await session.execute(
            select(CharityProject).where(CharityProject.id == project_id)
        )
        return db_project.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
