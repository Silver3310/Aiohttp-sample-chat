from auth.routes import setup_routers as auth_routers

from .common import STATIC_DIR


def setup_routers(app):
    """
    Setup routers from all applications
    :param app: web application
    :return: nothing, just configures the app
    """

    auth_routers(app)


def setup_static_routes(app):
    app.router.add_static(
        '/static/',
        path=STATIC_DIR,
        name='static'
    )
