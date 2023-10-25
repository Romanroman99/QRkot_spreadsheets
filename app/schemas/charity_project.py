from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator("name")
    def not_null_name(cls, value):
        if value is None or value == "":
            raise ValueError("Добавьте имя проекта!")
        return value

    @validator("description")
    def not_null_description(cls, value):
        if value is None or value == "":
            raise ValueError("Добавьте описание проекта!")
        return value

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1
        schema_extra = {
            "example": {
                "name": "Проект",
                "description": "Помощь котам",
                "full_amount": 3500,
            }
        }


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
