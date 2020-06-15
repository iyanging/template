# TODO: This is a sample file, Please remove it after imitative writing

from datetime import datetime
from enum import Enum
from typing import List, Optional, Text

from gql import enum_type
from pydantic import BaseModel, Field

from .employee import Employee
from .id import ID, IDInput


@enum_type
class MeetingStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 1
    FINISHED = 1


class Meeting(BaseModel):
    id: Optional[ID]
    name: Optional[Text]
    host: Optional[Employee]
    status: Optional[MeetingStatus]
    begin_at: Optional[datetime]
    end_at: Optional[datetime]
    location: Optional[Text]
    participants: Optional[List[Employee]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class MeetingList(BaseModel):
    data: Optional[List[Meeting]]
    total_count: Optional[int]


class CreateMeetingInput(BaseModel):
    name: Text
    host: IDInput
    status: MeetingStatus
    begin_at: datetime
    endAt: datetime
    location: Text
    participants: List[IDInput]


class MeetingFilterInput(BaseModel):
    id: Optional[ID]
    search: Optional[Text]
    status: Optional[MeetingStatus]
    is_deleted: Optional[bool]


class UpdateMeetingInput(BaseModel):
    id: ID
    name: Optional[Text]
    host: Optional[Employee]
    status: Optional[MeetingStatus]
    begin_at: Optional[datetime]
    end_at: Optional[datetime]
    location: Optional[Text]
    participants: Optional[List[Employee]]


class ExportMeetingsInput(BaseModel):
    ids: List[ID] = Field(op="in", column="id")
    is_deleted: Optional[bool]


class ExportMeetingInput(BaseModel):
    ids: List[ID]
    is_deleted: Optional[bool]
