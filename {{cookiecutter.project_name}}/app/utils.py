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


# def revoke_schedule_tasks(task: Task, args=List[Any]) -> None:
#     app = task.app
#     task_name = task.name
#
#     schedule_tasks = app.control.inspect().scheduled() or dict()
#     revoked_tasks = app.control.inspect().revoked() or dict()
#     revoked_task_ids = [task_id for _, task in revoked_tasks.items() for task_id in task]
#
#     scheduled_task_ids = []
#     for _, tasks in schedule_tasks.items():
#         for task in tasks:
#             if (
#                     (request := task.get('request'))
#                     and (task_id := request.get('id'))
#                     and (request.get('name') == task_name)
#                     and (request.get('args') == args)
#                     and (task_id not in revoked_task_ids)
#             ):
#                 scheduled_task_ids.append(task_id)
#     for task_id in scheduled_task_ids:
#         app.control.revoke(task_id)


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
