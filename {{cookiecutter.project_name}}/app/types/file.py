# TODO: This is a sample file, Please edit it after imitative writing

from typing import Text

from pydantic import BaseModel, Field

from .id import ID


class File(BaseModel):
    id: ID
    name: Text = Field(alias='filename')
    url: Text = ''
    checksum: Text = ''

    # for data loader
    thing_id: int = None
    spare_part_id: int = None
    thing_repair_id: int = None
    thing_maintenance_id: int = None
