"""
URLs dispatcher
"""
from .handlers import IndexView
from .handlers import LogInView
from .handlers import LogOutView
from .handlers import SignUpView


def setup_routers(app):
    app.router.add_get(
        '/',
        IndexView.get,
        name='index'
    )
    app.router.add_get(
        '/login',
        LogInView.get,
        name='login'
    )
    app.router.add_post(
        '/login',
        LogInView.post
    )
    app.router.add_get(
        '/signup',
        SignUpView.get,
        name='signup'
    )
    app.router.add_post(
        '/signup',
        SignUpView.post,
        name='signup'
    )
    app.router.add_get(
        '/logout',
        LogOutView.get,
        name='logout'
    )
