from datetime import datetime
from unittest.mock import MagicMock

from app.resolvers.utils import datetime_to_ymd, export_excel


def test_export_excel():
    record = MagicMock(a='a', b='b')
    header = ['A', 'B']
    cols = [('a',), ('b', lambda x: x)]
    content = export_excel([record], header, cols)
    assert type(content) == str


def test_datetime_to_ymd():
    time = datetime(year=2020, month=5, day=15)
    time_str = datetime_to_ymd(time)
    assert time_str == "2020-05-15"
    time_str = datetime_to_ymd(None, default="")
    assert time_str == ""
