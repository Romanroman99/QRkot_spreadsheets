from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse
from app.services.investing import investing

router = APIRouter()


@router.post(
    "/",
    response_model=DonationResponse,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Создает новое пожертвование.
    """
    new_donation = await donation_crud.create(donation, session, user)
    await investing(new_donation, CharityProject, session)
    return new_donation


@router.get(
    "/",
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=List[DonationResponse],
    response_model_exclude={"user_id"},
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список пожертвований пользователя.
    """
    return await donation_crud.get_user(user, session)
