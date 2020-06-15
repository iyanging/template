from typing import Iterable

from gql import mutate, query
from gql.parser import parse_info
from sqlalchemy import desc

from app import types
from app.db import models, transaction
from app.resolvers import utils
from app.utils import add_on_commit_task


@mutate
@transaction
async def create_meeting(_, info, input: dict) -> types.Meeting:
    obj_in = types.CreateMeetingInput(**input)
    meeting_id = await models.Meeting.objects.create(obj_in)

    await models.MeetingParticipant.objects.create_many(
        [dict(meeting_id=meeting_id, employee_id=v) for v in obj_in.participants]
    )

    add_on_commit_task(info, lambda: utils.begin_meeting_task(meeting_id, obj_in.begin_at))

    return await get_meeting(_, info, meeting_id)


@query("meeting")
async def get_meeting(*_, id: types.ID) -> types.Meeting:
    filter_obj = types.MeetingFilterInput(id=id, is_deleted=False)
    return await models.Meeting.objects.filter_by_model(filter_obj)


@query("meetings")
async def list_meetings(
    _, info, offset: int = None, limit: int = None, filter: dict = None
) -> types.MeetingList:
    filter_obj = (
        types.MeetingFilterInput(is_deleted=False, **filter)
        if filter
        else types.MeetingFilterInput(is_deleted=False)
    )
    meta = parse_info(info, depth=2)
    q = (
        models.Meeting.objects.filter_by_model(filter_obj)
        .order_by(desc("created_at"))
        .offset(offset)
        .limit(limit)
        .load(meta)
    )
    return types.MeetingList(data=await q.all(), total_count=await q.count())


@mutate
@transaction
async def update_meeting(_, info, input: dict) -> types.Meeting:
    obj_in = types.UpdateMeetingInput(**input)
    await models.Meeting.objects.filter_by(id=obj_in.id).update(obj_in)

    if obj_in.participants is not None:
        await models.MeetingParticipant.objects.update_m2m(
            "meeting_id", "employee_id", obj_in.id, obj_in.participants
        )

    return await get_meeting(_, info, obj_in.id)


@mutate
@transaction
async def delete_meeting(*_, input: dict) -> Iterable[types.ID]:
    return await models.Meeting.objects.filter_by_model(
        types.MeetingFilterInput(**input)
    ).soft_delete()


# TODO:
@query("exportMeetings")
async def export_meetings(_, info, input: dict) -> types.RawFile:
    # loader = info.context["loaders"]["meeting_participant"]
    pass
