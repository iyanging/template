# TODO: This is a sample file, Please remove it after imitative writing

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app import types
from app.db.base_class import Base, Enum, SoftDeleteMixin, TimeMixin
from app.db.models.employee import Employee
from app.db.query import Query


class MeetingQuery(Query):
    def lazy_build(self):
        return (
            self.lazy_load()
            .execute_relationships()
            .add_columns(Meeting.host_id, Employee.name.label("host.name"))
        )


class Meeting(Base, TimeMixin, SoftDeleteMixin):
    __tablename__ = "meeting"
    __schema__ = types.Meeting

    name = Column(String, nullable=False, unique=True)
    host_id = Column(None, ForeignKey("employee.id"), index=True)
    status = Column(Enum(types.MeetingStatus), nullable=False)
    beginAt = Column(DateTime(timezone=True), nullable=False)
    endAt = Column(DateTime(timezone=True), nullable=False)
    location = Column(String, nullable=False)

    host = relationship("Employee", backref="meeting", innerjoin=True)


class MeetingParticipant(Base):
    __tablename__ = "meeting_participant"

    meeting_id = Column(None, ForeignKey("meeting.id", ondelete="CASCADE"), index=True)
    employee_id = Column(None, ForeignKey("employee.id", ondelete='CASCADE'))
