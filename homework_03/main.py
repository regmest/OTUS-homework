"""
Домашнее задание №3
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio
from models import Base, engine, User, Post, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from jsonplaceholder_requests import get_all_data


async def create_tables():
    logger.info("Starting to create tables")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Finishing to create tables")


async def add_user_item(data):
    logger.info("Starting to add user data into user table")

    async with async_session() as session:
        session: AsyncSession

        async with session.begin():
            logger.info("Starting to add users")
            session.add(User(**user_data) for user_data in data)
            logger.info("Finishing to add users")

    logger.info("Finishing to add user data into user table")


async def add_post_item(data):
    logger.info("Starting to add post data into post table")

    async with async_session() as session:
        session: AsyncSession

        async with session.begin():
            session.add(Post(**post_data) for post_data in data)

    logger.info("Finishing to add post data into post table")


async def async_main():
    logger.info("Starting async_main")

    await create_tables()
    user_data, post_data = await get_all_data()
    coros = [
        add_user_item(user_data),
        add_post_item(post_data)
    ]
    coro = asyncio.wait({asyncio.create_task(coro) for coro in coros})
    await coro
    logger.info("Finishing async_main")


def main():
    logger.info("Starting main")
    asyncio.run(async_main())
    logger.info("Finishing main")


if __name__ == "__main__":
    main()

