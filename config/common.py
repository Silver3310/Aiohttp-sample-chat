"""
Common config for the application
"""
from os.path import isfile
from os.path import join
import pathlib

from envparse import env


# load env variables
if isfile('.env'):
    env.read_envfile('.env')

DEBUG = env.bool('DEBUG', default=False)
APP_NAME = env.str('APP_NAME', default='Sample Chat')

REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.str('REDIS_PORT')

MONGO_HOST = env.str('MONGO_HOST')
MONGO_DB_NAME = env.str('MONGO_DB_NAME')

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
STATIC_DIR = join(PROJECT_ROOT, 'static')
