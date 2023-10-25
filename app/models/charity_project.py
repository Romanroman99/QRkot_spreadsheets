from sqlalchemy import Column, String

from .abstract_base import AbstractBase


class CharityProject(AbstractBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)
