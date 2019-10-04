import logging

import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import redis_storage
from aiohttp_session import setup
from aioredis.commands import Redis
from motor.motor_asyncio import AsyncIOMotorClient

from config.common import REDIS_HOST
from config.common import MONGO_DB_NAME
from config.common import MONGO_HOST


def main():
    """
    Run the application
    """
    app = web.Application()

    # save sessions thru redis
    print(REDIS_HOST)
    redis_pool = Redis(REDIS_HOST)
    setup(
        app,
        redis_storage.RedisStorage(redis_pool=redis_pool)
    )

    # use the jinja2 as a templating language
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(
            package_name='main',
            package_path='templates'
        ),
    )

    app['db'] = getattr(
        AsyncIOMotorClient(MONGO_HOST),
        MONGO_DB_NAME
    )

    logging.basicConfig(level=logging.DEBUG)  # console level debug
    web.run_app(app)


if __name__ == '__main__':
    main()
