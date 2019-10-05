import asyncio

import aioredis
from aiohttp_session import redis_storage
from aiohttp_session import setup

from config.common import REDIS_PORT
from config.common import REDIS_HOST


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
