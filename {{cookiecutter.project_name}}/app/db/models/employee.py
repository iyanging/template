from app import types
from app.db.base_class import Base, SoftDeleteMixin, TimeMixin
from sqlalchemy import Column, ForeignKey, String


class Employee(Base, TimeMixin, SoftDeleteMixin):
    __tablename__ = "employee"
    __schema__ = types.Employee

    name = Column(String, nullable=False)


class EmployeeImage(Base):
    __tablename__ = 'employee_images'

    employee_id = Column(None, ForeignKey('employee.id', ondelete='CASCADE'), index=True)
    image_id = Column(None, ForeignKey('file.id', ondelete='CASCADE'))
