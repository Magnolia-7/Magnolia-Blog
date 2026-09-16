from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import settings


@dataclass
class StoredObject:
    key: str
    size_bytes: int


class StorageBackend(ABC):
    provider = "unknown"

    @abstractmethod
    def put(
        self,
        key: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> StoredObject:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError

    def url_for(self, key: str | None) -> str | None:
        if not key:
            return None
        return f"{settings.MEDIA_BASE_URL.rstrip('/')}/{key.lstrip('/')}"


class LocalStorageBackend(StorageBackend):
    provider = "local"

    def __init__(self, root: str):
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path_for(self, key: str) -> Path:
        path = (self.root / key).resolve()
        if self.root not in path.parents:
            raise ValueError("Invalid storage key")
        return path

    def put(
        self,
        key: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> StoredObject:
        path = self._path_for(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return StoredObject(key=key, size_bytes=len(content))

    def delete(self, key: str) -> None:
        path = self._path_for(key)
        if path.exists():
            path.unlink()


class R2StorageBackend(StorageBackend):
    provider = "r2"

    def __init__(
        self,
        account_id: str,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str,
        public_base_url: str,
    ):
        self.bucket_name = bucket_name
        self.public_base_url = public_base_url.rstrip("/")
        self.client = boto3.client(
            service_name="s3",
            endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name="auto",
            config=Config(signature_version="s3v4"),
        )

    def put(
        self,
        key: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> StoredObject:
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType=content_type,
                CacheControl="public, max-age=2592000",
            )
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"R2 上传失败：{key}") from exc
        return StoredObject(key=key, size_bytes=len(content))

    def delete(self, key: str) -> None:
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"R2 删除失败：{key}") from exc

    def url_for(self, key: str | None) -> str | None:
        if not key:
            return None
        return f"{self.public_base_url}/{key.lstrip('/')}"


@lru_cache(maxsize=4)
def _get_storage(driver: str) -> StorageBackend:
    if driver == "local":
        return LocalStorageBackend(settings.UPLOAD_DIR)
    if driver == "r2":
        values = {
            "R2_ACCOUNT_ID": settings.R2_ACCOUNT_ID,
            "R2_ACCESS_KEY_ID": settings.R2_ACCESS_KEY_ID,
            "R2_SECRET_ACCESS_KEY": settings.R2_SECRET_ACCESS_KEY,
            "R2_BUCKET_NAME": settings.R2_BUCKET_NAME,
            "R2_PUBLIC_BASE_URL": settings.R2_PUBLIC_BASE_URL,
        }
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise RuntimeError(f"R2 配置不完整，缺少：{', '.join(missing)}")
        return R2StorageBackend(
            account_id=settings.R2_ACCOUNT_ID,
            access_key_id=settings.R2_ACCESS_KEY_ID,
            secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            bucket_name=settings.R2_BUCKET_NAME,
            public_base_url=settings.R2_PUBLIC_BASE_URL,
        )
    raise RuntimeError(
        f"不支持的图片存储驱动：{driver}"
    )


def get_storage(provider: str | None = None) -> StorageBackend:
    driver = (provider or settings.STORAGE_DRIVER).strip().lower()
    return _get_storage(driver)
