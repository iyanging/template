# TODO: This is a sample file, Please remove it after imitative writing

from datetime import datetime
from enum import Enum
from typing import Optional, Text, List

from gql import enum_type
from pydantic import BaseModel

from .id import ID
from .file import File


@enum_type
class MeetingStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 1
    FINISHED = 1


class Meeting(BaseModel):
    id: Optional[ID]
    name: Optional[Text]
    host: Optional[Text]
    status: Optional[MeetingStatus]
    beginAt: Optional[datetime]
    endAt: Optional[datetime]
    location: Optional[Text]
    participants: Optional[List[Text]]
    "the image of signature"
    signature: Optional[File]
