from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase


class Message:
    """
    Message model
    """

    def __init__(self):
        pass

    @staticmethod
    async def save(
            db: AsyncIOMotorDatabase,
            user_id: str,
            msg: str
    ):
        """Save a message"""

        result = await db.messages.insert_one({
            'user_id': user_id,
            'msg': msg,
            'time': datetime.now()
        })
        return result

    @staticmethod
    async def get_messages(
            db: AsyncIOMotorDatabase
    ):
        """Get the messages to load"""

        # collection.objects returns a lazy QuerySet
        messages = await db.messages.find().sort(
            [('time', 1)]
        ).to_list(length=None)

        return messages
