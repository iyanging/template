import asyncio
from functools import partial, wraps
from typing import Any, Callable, Coroutine, Mapping, Sequence

ON_COMMIT_TASKS = 'on_commit_tasks'


def get_attr(obj: Any, key: str) -> Any:
    return obj[key] if isinstance(obj, Mapping) else getattr(obj, key, None)


def init_db(func=None, *, db=None):
    if func is None:
        return partial(init_db, db=db)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not db.is_connected:
            await db.connect()
        try:
            result = await func(*args, **kwargs)
        finally:
            if db.is_connected:
                await db.disconnect()
        return result

    return wrapper


def init_redis(func=None, *, redis=None):
    if func is None:
        return partial(init_redis, redis=redis)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not redis.is_connected:
            await redis.connect()
        try:
            result = await func(*args, **kwargs)
        finally:
            if redis.is_connected:
                await redis.disconnect()
        return result

    return wrapper


def async_celery_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        asyncio.run(func(*args, **kwargs))

    return wrapper


class OnCommitTasks:
    def __init__(self, tasks: Sequence[Callable] = None):
        if tasks is None:
            tasks = []
        self.tasks = list(tasks)

    def add_task(self, func: Callable,) -> None:
        self.tasks.append(func)


def init_on_commit_tasks(info):
    if info and hasattr(info, 'context') and isinstance(info.context, dict):
        info.context[ON_COMMIT_TASKS] = OnCommitTasks()


def add_on_commit_task(info, func: Callable):
    info.context[ON_COMMIT_TASKS].add_task(func)


async def exec_on_commit_tasks(info):
    if (
        info
        and hasattr(info, 'context')
        and isinstance(info.context, dict)
        and (on_commit_tasks := info.context.get(ON_COMMIT_TASKS))
    ):
        for task in on_commit_tasks.tasks:
            result = task()
            if isinstance(result, Coroutine):
                await result
