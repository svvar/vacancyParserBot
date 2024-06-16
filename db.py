import datetime
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


db_url = 'sqlite+aiosqlite:///requests.sqlite'
engine = create_async_engine(db_url, echo=False)
Base = declarative_base()


class Request(Base):
    __tablename__ = 'requests'
    id = sa.Column(sa.Integer, primary_key=True)
    datetime = sa.Column(sa.DateTime())
    vacancy_count = sa.Column(sa.Integer)

    def __repr__(self):
        return f'{self.datetime} {self.vacancy_count}'


async def save_request(vacancy_count):
    async with AsyncSession(engine) as session:
        async with session.begin():
            new_request = Request(datetime=datetime.datetime.now(), vacancy_count=vacancy_count)
            session.add(new_request)
        await session.commit()


async def get_by_day(date):
    async with AsyncSession(engine) as session:
        result = await session.execute(sa.select(Request).filter(func.DATE(Request.datetime) == date))
        return result.scalars().all()
