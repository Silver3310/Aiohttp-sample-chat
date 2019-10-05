import aiohttp_jinja2
from aiohttp import web
from aiohttp import WSMsgType
from aiohttp_session import get_session

from auth.models import User
from chat.models import Message


class MessagesListView(web.View):
    """
    Show all messages
    """

    @aiohttp_jinja2.template('chat/chat.html')
    async def get(self):
        messages = await Message.get_messages(db=self.app['db'])

        for message in messages:
            user = await User.get_user_by_id(
                db=self.app['db'],
                user_id=message['user_id']
            )
            message['user'] = user['first_name']
            message['email'] = user['email']

        return {'messages': messages}


class WebSocket(web.View):

    async def get(self):
        """
        Handling WebSockets
        """

        # create a socket
        ws = web.WebSocketResponse()
        await ws.prepare(self)

        session = await get_session(self)

        try:
            user = await User.get_user_by_id(
                db=self.app['db'],
                user_id=session['user']['_id']
            )
        except KeyError:
            # if the user is not authenticated
            location = self.app.router['login'].url_for()
            return web.HTTPFound(location=location)

        # for all current web sockets
        for _ws in self.app['websockets']:
            await _ws.send_str(f"{user['first_name']} joined!")

        self.app['websockets'].append(ws)

        async for msg in ws:

            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    # if it's a signal to close the socket, close the socket
                    await ws.close()
                else:
                    # otherwise, it's a message
                    message = await Message.save(
                        db=self.app['db'],
                        user_id=user['_id'],
                        msg=msg.data
                    )

                    # then notify others
                    for _ws in self.app['websockets']:
                        await _ws.send_str(
                            f"{user['first_name']} ({user['email']}): "
                            f"{msg.data}"
                        )

        self.app['websockets'].remove(ws)
        for _ws in self.app['websockets']:
            await _ws.send_str(
                f"{user['first_name']} ({user['email']}) disconnected"
            )

        return ws
