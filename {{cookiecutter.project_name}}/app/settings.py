# TODO: This is a sample file, Please edit it after imitative writing

import os
from pathlib import Path

from starlette.config import Config

ROOT_DIR = Path(__file__).parents[1]

READ_DOT_ENV_FILE = bool(os.environ.get('READ_DOT_ENV_FILE', default=False))

if READ_DOT_ENV_FILE:
    config = Config(str(ROOT_DIR / '.env'))
else:
    config = Config()

GRAPHQL_SCHEMA_FILE = config(
    'GRAPHQL_SCHEMA_FILE', cast=str, default=str(ROOT_DIR / 'schema.graphql')
)
GRAPHQL_PATH = config('GRAPHQL_PATH', default='/graphql/')

DEBUG = config('DEBUG', cast=bool, default=False)

TESTING = config('TESTING', cast=bool, default=False)

APP_ID = '4e6f0fd6-7e59-4860-b0c0-1255fb416507'

DATABASE_URL = config('DATABASE_URL', default='postgresql://postgres:postgres@postgres:5432/eam')
REDIS_URL = config('REDIS_URL', default='redis://redis:6379')
CELERY_BROKER = config('CELERY_BROKER', default='redis://redis:6379/0')

# file storage
FILE_ENDPOINT = config('FILE_ENDPOINT', default='minio:9000')
FILE_ACCESS_KEY = config('FILE_ACCESS_KEY', default='admin')
FILE_SECRET_KEY = config('FILE_SECRET_KEY', default='teletraan')
FILE_SECURE = config('FILE_SECURE', cast=bool, default=False)
FILE_BUCKET = config('FILE_BUCKET', default='eam')
FILE_REGION = config('FILE_REGION', default='cn-north-1')
FILE_MAX_AGE = config('FILE_MAX_AGE', cast=int, default=86400)

# APIGateway
ENABLE_KONG = config('ENABLE_KONG', cast=bool, default=False)
ENABLE_FILE_GATEWAY = config('ENABLE_FILE_GATEWAY', cast=bool, default=False)
FILE_GATEWAY_ENDPOINT = config('FILE_GATEWAY_ENDPOINT', default='http://localhost:8000/minio')

if DEBUG:
    LOG_LEVEL = config('LOG_LEVEL', default='DEBUG')
else:
    LOG_LEVEL = config('LOG_LEVEL', default='INFO')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[%(asctime)s] [%(levelname)s] [%(message)s]',},
        'complex': {
            'format': '[%(asctime)s] [%(process)s] [%(name)s:%(module)s:%(lineno)d] [%(levelname)s] [%(message)s]',
        },
    },
    'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'}},
    'root': {'level': LOG_LEVEL, 'handlers': ['console']},
}
