from datetime import timedelta

from app import settings
from minio import Minio
from starlette.datastructures import UploadFile

minio = Minio(
    settings.FILE_ENDPOINT,
    access_key=settings.FILE_ACCESS_KEY,
    secret_key=settings.FILE_SECRET_KEY,
    secure=settings.FILE_SECURE,
)


def init_bucket():
    if not minio.bucket_exists(settings.FILE_BUCKET):
        minio.make_bucket(settings.FILE_BUCKET)


def upload_file(file: UploadFile, length: int, name: str = None):
    filename = name or file.filename
    return minio.put_object(settings.FILE_BUCKET, filename, file.file, length, file.content_type)


def get_link(file_name):
    url = minio.presigned_get_object(
        settings.FILE_BUCKET, file_name, expires=timedelta(seconds=settings.FILE_MAX_AGE)
    )
    if settings.ENABLE_FILE_GATEWAY:
        path_index = url.find(f'/{settings.FILE_BUCKET}')
        url = settings.FILE_GATEWAY_ENDPOINT + url[path_index:]
    return url


init_bucket()
