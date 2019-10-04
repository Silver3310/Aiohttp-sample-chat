import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import redis_storage, setup
from aioredis.commands import Redis

from config.common import REDIS_HOST


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

    web.run_app(app)


if __name__ == '__main__':
    main()
