# TODO: This is a sample file, Please edit it after imitative writing

from typing import Optional, Text

from pydantic import BaseModel


class RawFile(BaseModel):
    data: Optional[Text]
    name: Optional[Text]
