import logging.config
from importlib import import_module

from app import settings
from app.db import database
from app.loaders import context_builder
from app.redis import redis
from stargql import GraphQL

# register resolvers
import_module('app.resolvers')

# init logging config
logging.config.dictConfig(settings.LOGGING)


async def startup():
    await database.connect()
    await redis.connect()


async def shutdown():
    await database.disconnect()
    await redis.disconnect()


app = GraphQL(
    schema_file=settings.GRAPHQL_SCHEMA_FILE,
    path=settings.GRAPHQL_PATH,
    on_startup=[startup],
    on_shutdown=[shutdown],
    debug=settings.DEBUG,
    context_builder=context_builder,
)
