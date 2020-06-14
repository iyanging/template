# TODO: This is a sample file, Please remove it after imitative writing

from sqlalchemy import Column, DateTime, Float, ForeignKey, String

from app import types
from app.db.base_class import Base, Enum, SoftDeleteMixin, TimeMixin


class Meeting(Base, TimeMixin, SoftDeleteMixin):
    __tablename__ = 'meeting'
    __schema__ = types.Meeting

    name = Column(String, nullable=False, unique=True)
    host_id = Column(None, ForeignKey('employee.id', ondelete='CASCADE'), index=True)
    status = Column(Enum(types.MeetingStatus), nullable=False)
    beginAt = Column(DateTime(timezone=True), nullable=False)
    endAt = Column(DateTime(timezone=True), nullable=False)
    location = Column(String, nullable=False)
    participants = Column(ARRAY)
    "the image of signature"
    signature: [File!]