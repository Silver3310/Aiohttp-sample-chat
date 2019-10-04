"""
Handlers (views) for the User model
"""
import hashlib

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from pymongo.results import InsertOneResult

from .models import User


class IndexView(web.View):
    """
    Index view
    """

    @aiohttp_jinja2.template('index.html')
    async def get(self):  # <Request GET / >
        """Show the introduction for a user"""

        return dict()


class LogInView(web.View):
    """
    Login view
    """

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        """Show the form for entering data"""

        return dict()

    async def post(self):  # <Request POST /login >
        """Singing up"""

        # self.post() is a coroutine object
        data = await self.post()  # take all the data from the form
        email = data['email']
        password = data['password']

        user = await User.get_user(
            db=self.request.app['db'],
            email=email
        )

        if user.get('error'):
            location = self.request.app['db'].router['login'].url_for()
            return web.HTTPFound(location=location)

        if user['password'] == hashlib.sha256(
                password.encode('utf-8')
        ).hexdigest():
            session = await get_session(self)
            session['user'] = user

        location = self.request.app['db'].router['index'].url_for()
        return web.HTTPFound(location=location)  # 302 moved temporarily


class SignUpView(web.View):
    """
    Sign up view
    """

    @aiohttp_jinja2.template('signup.html')
    async def get(self):
        """Show the form for entering data"""

        return dict()

    async def post(self):
        """Singing up a user"""

        data = await self.post()
        result: InsertOneResult = await User.create_new_user(
            db=self.request.app['db']['db'],
            data=data
        )
        # if result has an attribute 'get' it means that it's a dict and
        # contains an error
        if not result or hasattr(result, 'get'):
            location = self.request.app['db'].router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.request.app['db'].router['login'].url_for()
        return web.HTTPFound(location=location)


class LogOutView(web.View):
    """
    Logout view
    """

    async def get(self):
        """log out"""
        session = await get_session(self)
        del session['user']

        location = self.request.app['db'].router['login'].url_for()
        return web.HTTPFound(location=location)
