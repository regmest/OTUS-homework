"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""

import asyncio

from aiohttp import ClientSession
from loguru import logger
from dataclasses import dataclass


@dataclass
class Service:
    name: str
    url: str
    fields_to_get: list


USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"

user_service = Service("users_data", USERS_DATA_URL, ["address", "id", "name", "username", "email", "phone"])
post_service = Service("posts_data", POSTS_DATA_URL, ["id", "userId", "title", "body"])


async def fetch_json(session: ClientSession, url: str) -> dict:
    """ Получаем ответ от сервиса в виде json"""
    async with session.get(url) as response:
        return await response.json()


async def fetch_data(service: Service) -> list:
    """ Вытаскиваем из ответа сервиса нужные поля """
    logger.info("Starting to fetch data from {}", service.name)

    async with ClientSession() as session:
        all_data = await fetch_json(session, service.url)

    data = []
    # выбираем нужные поля
    for dict_item in all_data:
        short_dict_item = {}
        for key, value in dict_item.items():
            if key in service.fields_to_get:
                # пытаюсь вытащить город из словаря address поле city и подменить address -> city
                if service.name == "users_data" and key == "address":
                    key, value = "city", dict_item["address"]["city"]
                short_dict_item[key] = value
        data.append(short_dict_item)

    logger.info("Finished to fetch data from {}", service.name)
    return data


async def get_all_data():
    """ Собираем данные """
    logger.info("Starting to gather data from services")

    user_data, post_data = await asyncio.gather(
        fetch_data(user_service),
        fetch_data(post_service)
    )

    await asyncio.sleep(0.1)  # чтобы обойти баг на windows https://github.com/encode/httpx/issues/914
    # Была ошибка: RuntimeError: Event loop is closed

    # logger.info("USER DATA: {}, POST DATA: {}", user_data, post_data)
    logger.info("Finished to gather data from services")
    return user_data, post_data


if __name__ == "__main__":
    asyncio.run(get_all_data())
