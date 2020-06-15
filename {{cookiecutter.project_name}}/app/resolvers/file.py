import time
from typing import List

from app import types
from app.db import transaction
from app.db.models import File
from app.file_storage import minio
from app.utils import get_attr
from gql import field_resolver, mutate
from minio.helpers import get_md5_base64digest
from starlette.datastructures import UploadFile


async def single_upload(file: UploadFile) -> types.File:
    # TODO: different user
    filename = file.filename

    with file.file:
        data = await file.read()
        checksum = get_md5_base64digest(data)
        file_objs = await File.objects.filter_by_name_or_checksum(filename, checksum).all()
        for file_obj in file_objs:
            if file_obj.checksum == checksum:
                return file_obj
            if file_obj.name == filename:
                filename = f'{int(time.time())}_{filename}'

        length = file.file.tell()
        await file.seek(0)
        minio.upload_file(file, length, name=filename)
        file_id = await File.objects.create(
            types.CreateFileInput(filename=filename, checksum=checksum, length=length)
        )
        return types.File(id=file_id, filename=filename)


@field_resolver('File', 'url')
def get_url(parent, info) -> str:
    return minio.get_link(get_attr(parent, 'name'))


@mutate
@transaction
async def upload_file(parent, info, file: UploadFile) -> File:
    return await single_upload(file)


@mutate
@transaction
async def upload_files(parent, info, files: List[UploadFile]) -> List[File]:
    return [await single_upload(file) for file in files]
