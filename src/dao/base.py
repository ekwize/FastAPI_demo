from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.database import Base, async_session

# from src.logger import logger


class BaseDAO:
    model: Base = None

    @classmethod
    async def find_by_id(cls, model_id: id):
        async with async_session() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
        #         return result.mappings().first()
        # except (SQLAlchemyError, Exception) as e:
        #     if isinstance(e, SQLAlchemyError):
        #         msg = "Database Exc: Cannot insert data into table"
        #     elif isinstance(e, Exception):
        #         msg = "Unknown Exc: Cannot insert data into table"

        #     # logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
        #     # return None

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    
    # @classmethod
    # async def add_bulk(cls, *data):
    #     # Для загрузки массива данных [{"id": 1}, {"id": 2}]
    #     # мы должны обрабатывать его через позиционные аргументы *args.
    #     try:
    #         query = insert(cls.model).values(*data).returning(cls.model.id)
    #         async with async_session_maker() as session:
    #             result = await session.execute(query)
    #             await session.commit()
    #             return result.mappings().first()
    #     except (SQLAlchemyError, Exception) as e:
    #         if isinstance(e, SQLAlchemyError):
    #             msg = "Database Exc"
    #         elif isinstance(e, Exception):
    #             msg = "Unknown Exc"
    #         msg += ": Cannot bulk insert data into table"

    #         logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
    #         return None