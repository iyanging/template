from itertools import groupby
from operator import attrgetter
from typing import Any, Callable, List, Sequence, TypeVar

from dataloader import DataLoader

from app.db.models import EmployeeImage, File, Meeting, MeetingParticipant
from app.types import ID

KT, VT = TypeVar("KT"), TypeVar("VT")

KEY_FUNCTION = Callable[[VT], Any]


def sort(keys: Sequence[KT], values: Sequence[VT], *, key_fn: KEY_FUNCTION) -> List[Any]:
    """
    Sort values sequence by keys sequence.
    """
    value_map = {key_fn(v): v for v in values}
    return list(map(lambda k: value_map.get(k), keys))


def group_sort(keys: Sequence[KT], values: Sequence[VT], *, key_fn: KEY_FUNCTION) -> List[Any]:
    """
    Sort and group value sequence by key sequence.

    Often used in one to many and many to many cases.
    """
    values = sorted(values, key=key_fn)
    value_map = {key: list(data) for key, data in groupby(values, key=key_fn)}
    return list(map(lambda k: value_map.get(k), keys))


async def list_employee_images(employee_ids: List[ID]) -> List[Any]:
    data = (
        await File.objects.join(EmployeeImage)
        .filter(EmployeeImage.employee_id.in_(employee_ids))
        .add_columns(EmployeeImage.employee_id)
        .all()
    )
    return group_sort(employee_ids, data, key_fn=attrgetter("employee_id"))


async def list_meeting_participants(meeting_ids: List[ID]) -> List[Any]:
    data = (
        await Meeting.objects.join(MeetingParticipant)
        .filter(MeetingParticipant.meeting_id.in_(meeting_ids))
        .add_columns(MeetingParticipant.meeting_id)
        .all()
    )
    return group_sort(meeting_ids, data, key_fn=attrgetter("meeting_id"))


def context_builder():
    return {
        "loaders": {
            "employee_image": DataLoader(list_employee_images),
            "meeting_participant": DataLoader(list_meeting_participants),
        }
    }
