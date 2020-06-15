from sqlalchemy import Column, Integer, String, or_

from app import types
from app.db.base_class import Base, Query, add_objects


class FileQuery(Query):
    def filter_by_name_or_checksum(self, name: str, checksum: str):
        return self.filter(or_(self.table.c.filename == name, self.table.c.checksum == checksum))


@add_objects(FileQuery)
class File(Base):
    __tablename__ = "file"
    __schema__ = types.File

    filename = Column(String)
    checksum = Column(String)
    length = Column(Integer)
