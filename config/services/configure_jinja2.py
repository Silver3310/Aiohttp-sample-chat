import aiohttp_jinja2
import jinja2

from config.middlewares import current_user_ctx_processor


def configure_jinja2(app):
    """
    Configure Jinja2
    """

    # use the jinja2 as a templating language
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(
            package_name='main',
            package_path='templates'
        ),
        context_processors=[current_user_ctx_processor]
    )
