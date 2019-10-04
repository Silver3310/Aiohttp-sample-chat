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

    @aiohttp_jinja2.template('auth/index.html')
    async def get(self):  # <Request GET / >
        """Show the introduction for a user"""

        return dict()


class LogInView(web.View):
    """
    Login view
    """

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        """Show the form for entering data"""

        return dict()

    async def post(self):  # <Request POST /login >
        """
        Login

        If it fails, the page updates
        If it succeeds, the user is sent to the Index page
        """

        # take all the data from the form
        data = await self.post()
        email = data['email']
        password = data['password']

        user = await User.get_user(
            db=self.app['db'],
            email=email
        )

        if user.get('error'):
            location = self.app.router['login'].url_for()
            return web.HTTPFound(location=location)

        if user['password'] == hashlib.sha256(
                password.encode('utf-8')
        ).hexdigest():
            session = await get_session(self)
            session['user'] = user

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)  # 302 moved temporarily


class SignUpView(web.View):
    """
    Sign up view
    """

    @aiohttp_jinja2.template('auth/signup.html')
    async def get(self):
        """Show the form for entering data"""

        return dict()

    async def post(self):
        """
        Signing up a user

        If it fails, the page updates
        If it succeeds, the user is sent to the Login page
        """

        data = await self.post()
        result: InsertOneResult = await User.create_new_user(
            db=self.app['db'],
            data=data
        )
        # if result has an attribute 'get' it means that it's a dict and
        # contains an error
        if not result or hasattr(result, 'get'):
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class LogOutView(web.View):
    """
    Logout view

    Redirects to the Login page
    """

    async def get(self):
        """log out"""
        session = await get_session(self)
        # clear the cookie
        session.invalidate()

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)
