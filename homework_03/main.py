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

# -*- coding: utf8 -*-

import asyncio
from models import Base, engine, User, Post, async_session, conn
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
            for user_data in data:
                # logger.info("Starting to add this user data: {}", user_data)
                user = User(
                    id=user_data["id"],
                    name=user_data["name"],
                    username=user_data["username"],
                    email=user_data["email"],
                    city=user_data["city"],
                    phone=user_data["phone"],
                    )
                session.add(user)

    logger.info("Finishing to add user data into user table")


async def add_post_item(data):
    logger.info("Starting to add post data into post table")

    async with async_session() as session:
        session: AsyncSession

        async with session.begin():
            for post_data in data:
                # logger.info("Starting to add this post data: {}", post_data)
                post = Post(
                    userId=post_data["userId"],
                    id=post_data["id"],
                    title=post_data["title"],
                    body=post_data["body"]
                    )
                session.add(post)

    logger.info("Finishing to add post data into post table")


async def async_main():
    logger.info("Starting async_main")
    await create_tables()
    user_data, post_data = await get_all_data()
    # await add_user_item(user_data)
    # await add_post_item(post_data)
    coros = [
        add_user_item(user_data),
        add_post_item(post_data)
    ]
    coro = asyncio.wait({asyncio.create_task(coro) for coro in coros})
    await coro

    # logger.info("Closing PG connection")
    # conn.close()
    # logger.info("CONNECTION INFO: {}", conn)

    # await asyncio.sleep(0.1)  # чтобы обойти баг на windows https://github.com/encode/httpx/issues/914
    # # Была ошибка: RuntimeError: Event loop is closed

    logger.info("Finishing async_main")


def main():
    logger.info("Starting main")
    asyncio.run(async_main())
    logger.info("Finishing main")


if __name__ == "__main__":
    main()

