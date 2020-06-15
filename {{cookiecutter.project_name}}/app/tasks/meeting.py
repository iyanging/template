from app import types
from app.celery import app
from app.db import database
from app.db.models import Meeting
from app.redis import redis
from app.utils import async_celery_task, init_db, init_redis


@app.task(bind=True)
@async_celery_task
@init_redis(redis=redis)
@init_db(db=database)
async def begin_meeting(self, meeting_id):
    task_id = await redis.execute("GET", f"begin_meeting_task_{meeting_id}")

    if not task_id or task_id != self.request.id:
        return None

    if not await Meeting.objects.filter(Meeting.id == meeting_id).exists():
        return None

    update_obj = types.UpdateMeetingInput(id=meeting_id, status=types.MeetingStatus.IN_PROGRESS)
    await Meeting.objects.filter_by(id=meeting_id, is_deleted=False).update(update_obj)
