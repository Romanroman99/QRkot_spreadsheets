from datetime import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class AbstractBase(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, default=None)

    def __repr__(self):
        return (
            f"full_amount: {self.full_amount}, "
            f"invested_amount: {self.invested_amount}, "
            f"fully_invested: {self.fully_invested}, "
            f"create_date: {self.create_date}, "
            f"close_date: {self.close_date}"
        )
