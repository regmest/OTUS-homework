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
from models import Base, engine, User, Post, Session  # , conn
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

    async with Session() as session:
        session: AsyncSession

        async with session.begin():
            users_list = []
            for user_data in data:
                users_list.append(
                    User(
                        id=user_data["id"],
                        name=user_data["name"],
                        username=user_data["username"],
                        email=user_data["email"],
                        city=user_data["city"],
                        phone=user_data["phone"],
                    ))
            logger.info("Starting to add these users: {}", users_list)
            session.add_all(users_list)
            logger.info("Added all {} users", len(users_list))

    logger.info("Finishing to add user data into user table")


async def add_post_item(data):
    logger.info("Starting to add post data into post table")

    async with Session() as session:
        session: AsyncSession

        async with session.begin():
            posts_list = []
            for post_data in data:
                posts_list.append(
                    Post(
                        user_id=post_data["userId"],
                        id=post_data["id"],
                        title=post_data["title"],
                        body=post_data["body"]
                    ))
            logger.info("Starting to add these posts: {}", posts_list)
            session.add_all(posts_list)
            logger.info("Added all {} posts", len(posts_list))

    logger.info("Finishing to add post data into post table")


async def async_main():
    logger.info("Starting async_main")
    await create_tables()
    user_data, post_data = await get_all_data()

    await add_user_item(user_data)
    await add_post_item(post_data)

    # logger.info("Closing PG connection")
    # conn.close()
    # logger.info("CONNECTION INFO: {}", conn)

    logger.info("Finishing async_main")


def main():
    logger.info("Starting main")
    asyncio.run(async_main())
    logger.info("Finishing main")


if __name__ == "__main__":
    main()
