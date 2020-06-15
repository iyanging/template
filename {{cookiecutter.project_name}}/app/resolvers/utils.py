from datetime import datetime

from app import types
from app.redis import redis
from app.tasks import begin_meeting


async def begin_meeting_task(meeting_id: types.ID, begin_at: datetime):
    task = begin_meeting.apply_async((meeting_id,), eta=begin_at)
    await redis.execute('SET', f'start_inspection_task_{meeting_id}', task.id)
