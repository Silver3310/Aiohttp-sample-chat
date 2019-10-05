import logging
import asyncio

import aioredis
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import redis_storage
from aiohttp_session import setup
from motor.motor_asyncio import AsyncIOMotorClient

from config.common import REDIS_HOST
from config.common import REDIS_PORT
from config.common import MONGO_DB_NAME
from config.common import MONGO_HOST

from config.routes import setup_routers
from config.routes import setup_static_routes

from config.middlewares import current_user_ctx_processor


async def make_redis_pool():
    """
    Redis client bound to pool of connections (auto-reconnecting)
    """

    redis_address = (REDIS_HOST, REDIS_PORT)
    return await aioredis.create_redis_pool(redis_address, timeout=1)


def configure_redis(app):
    """
    Configure Redis for sessions
    """

    # save sessions thru redis
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    setup(
        app,
        redis_storage.RedisStorage(
            redis_pool=redis_pool,
            cookie_name='FIXATED'
        )
    )

    async def dispose_redis_pool(app_):
        """Gracefully closing underlying connection"""
        redis_pool.close()
        await redis_pool.wait_closed()

    app.on_cleanup.append(dispose_redis_pool)


def configure_web_sockets(app):
    """
    Configure WebSockets
    """

    async def on_shutdown(app):
        for ws in app['websockets']:
            await ws.close(
                code=1001,
                message='Server shutdown'
            )

    app.on_cleanup.append(on_shutdown)

    # a list of sockets to close after use
    app['websockets'] = list()


def configure_jinja2(app):
    """
    Configure Jinja2
    """

    # use the jinja2 as a templating language
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(
            package_name='main',
            package_path='templates'
        ),
        context_processors=[current_user_ctx_processor]
    )


def configure_db(app):
    """
    Configure the database
    """

    app['db'] = getattr(
        AsyncIOMotorClient(MONGO_HOST),
        MONGO_DB_NAME
    )


def main():
    """
    Run the application
    """
    app = web.Application()

    # configurations
    configure_redis(app)
    configure_jinja2(app)
    configure_db(app)
    configure_web_sockets(app)

    # URLs dispatcher
    setup_routers(app)
    setup_static_routes(app)

    # console level debug
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)


if __name__ == '__main__':
    main()
