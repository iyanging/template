# TODO: This is a sample file, Please edit it after imitative writing

from functools import wraps

from databases import Database

from app import settings
from app.utils import exec_on_commit_tasks, init_on_commit_tasks

if settings.TESTING:
    database = Database(settings.DATABASE_URL, force_rollback=True)
else:
    database = Database(settings.DATABASE_URL)


def transaction(func):
    @wraps(func)
    async def wrap(parent, info, *args, **kwargs):
        tx = await database.transaction()
        init_on_commit_tasks(info)

        try:
            res = await func(parent, info, *args, **kwargs)
        except Exception as exc:
            await tx.rollback()
            raise exc
        else:
            await tx.commit()
            await exec_on_commit_tasks(info)

            return res

    return wrap
