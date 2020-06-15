# TODO: This is a sample file, Please remove it after imitative writing

from typing import List, Optional, Text

from pydantic import BaseModel

from .file import File
from .id import ID, IDInput


class Employee(BaseModel):
    id: Optional[ID]
    name: Optional[Text]
    images: Optional[List[File]]


class CreateEmployeeInput(BaseModel):
    name: Text
    images: IDInput


class EmployeeFilterInput(BaseModel):
    id: Optional[ID]
    search: Optional[Text]
    is_deleted: Optional[bool]
