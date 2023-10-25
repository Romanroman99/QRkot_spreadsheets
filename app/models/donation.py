from sqlalchemy import Column, ForeignKey, Integer, String

from .abstract_base import AbstractBase


class Donation(AbstractBase):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(String)
