from aiohttp_session import get_session

from auth.models import User


async def current_user_ctx_processor(request):
    """
    Add current user to the context

    It provides us with {{ current_user }} and {{ is_anonymous }} in templates
    """

    session = await get_session(request)
    user = None
    is_anonymous = True

    if 'user' in session:
        user_id = session['user']['_id']
        user = await User.get_user_by_id(
            db=request.app['db'],
            user_id=user_id
        )
        if user:
            is_anonymous = not bool(user)

    return dict(
        current_user=user,
        is_anonymous=is_anonymous
    )
