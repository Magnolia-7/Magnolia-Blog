from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings


@dataclass
class StoredObject:
    key: str
    size_bytes: int


class StorageBackend(ABC):
    provider = "unknown"

    @abstractmethod
    def put(self, key: str, content: bytes) -> StoredObject:
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

    def put(self, key: str, content: bytes) -> StoredObject:
        path = self._path_for(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return StoredObject(key=key, size_bytes=len(content))

    def delete(self, key: str) -> None:
        path = self._path_for(key)
        if path.exists():
            path.unlink()


def get_storage() -> StorageBackend:
    if settings.STORAGE_DRIVER == "local":
        return LocalStorageBackend(settings.UPLOAD_DIR)
    raise RuntimeError(
        f"Storage driver '{settings.STORAGE_DRIVER}' is not configured. "
        "Cloudflare R2 support can be added without changing callers."
    )
