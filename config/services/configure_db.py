from motor.motor_asyncio import AsyncIOMotorClient

from config.common import MONGO_HOST
from config.common import MONGO_DB_NAME


def configure_db(app):
    """
    Configure the database
    """

    app['db'] = getattr(
        AsyncIOMotorClient(MONGO_HOST),
        MONGO_DB_NAME
    )
