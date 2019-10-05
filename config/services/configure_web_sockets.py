def configure_web_sockets(app):
    """
    Configure WebSockets
    """

    async def on_shutdown(app):
        for ws in app['websockets']:
            await ws.close(
                code=1001,
                message='Server shutdown'
            )

    app.on_cleanup.append(on_shutdown)

    # a list of sockets to close after use
    app['websockets'] = list()
