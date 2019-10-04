from auth.routes import setup_routers as auth_routers


def setup_routers(app):
    """
    Setup routers from all applications
    :param app: web application
    :return: nothing, just configures the app
    """

    auth_routers(app)
