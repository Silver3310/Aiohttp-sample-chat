"""
URLs dispatcher
"""
from .handlers import MessagesListView
from .handlers import WebSocket


def setup_routers(app):
    app.router.add_get(
        '/chat',
        MessagesListView.get,
        name='chat'
    )
    app.router.add_get(
        '/ws',
        WebSocket.get,
        name='websocket'
    )

