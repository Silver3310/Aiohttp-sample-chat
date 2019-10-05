import logging

from aiohttp import web

from config.routes import setup_routers
from config.routes import setup_static_routes

from config.services.configure_web_sockets import configure_web_sockets
from config.services.configure_db import configure_db
from config.services.configure_jinja2 import configure_jinja2
from config.services.configure_redis import configure_redis


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
