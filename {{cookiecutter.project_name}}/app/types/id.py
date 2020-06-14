# TODO: This is a sample file, Please edit it after imitative writing

from typing import NewType

from pydantic import BaseModel

ID = NewType('ID', int)


class IDInput(BaseModel):
    id: ID

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return int(v['id'])
