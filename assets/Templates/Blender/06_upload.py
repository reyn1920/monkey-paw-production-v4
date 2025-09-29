"""Upload API endpoints for file upload and management."""

from typing import Optional
from datetime import datetime
import logging
import hashlib
import mimetypes
from pathlib import Path
import uuid

# Simple fallback classes for missing dependencies


class APIRouter:
    def __init__(self, **kwargs):
        self.routes = []

    def get(self, path: str, **kwargs):
        def decorator(func):
            self.routes.append({"method": "GET", "path": path, "func": func})
            return func

        return decorator

    def post(self, path: str, **kwargs):
        def decorator(func):
            self.routes.append({"method": "POST", "path": path, "func": func})
            return func

        return decorator

    def delete(self, path: str, **kwargs):
        def decorator(func):
            self.routes.append({"method": "DELETE", "path": path, "func": func})
            return func

        return decorator


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class BaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class UploadFile:
    def __init__(self, filename: str = "", content_type: str = "", file=None):
        self.filename = filename
        self.content_type = content_type
        self.file = file

    async def read(self) -> bytes:
        if self.file:
            return await self.file.read()
        return b""

    async def write(self, data: bytes):
        if self.file:
            await self.file.write(data)


class status:
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_404_NOT_FOUND = 404
    HTTP_200_OK = 200
    HTTP_400_BAD_REQUEST = 400
    HTTP_413_REQUEST_ENTITY_TOO_LARGE = 413
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415


# Logger setup
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".doc", ".docx"}

# Ensure upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)

# Pydantic Models


class FileInfo(BaseModel):
    def __init__(
        self,
        file_id: str = "",
        filename: str = "",
        original_filename: str = "",
        content_type: str = "",
        size: int = 0,
        upload_date: Optional[datetime] = None,
        file_hash: str = "",
        **kwargs,
    ):
        self.file_id = file_id
        self.filename = filename
        self.original_filename = original_filename
        self.content_type = content_type
        self.size = size
        self.upload_date = upload_date or datetime.utcnow()
        self.file_hash = file_hash
        super().__init__(**kwargs)


class UploadResponse(BaseModel):
    def __init__(
        self,
        success: bool = False,
        message: str = "",
        file_info: Optional[FileInfo] = None,
        **kwargs,
    ):
        self.success = success
        self.message = message
        self.file_info = file_info
        super().__init__(**kwargs)


class FileListResponse(BaseModel):
    def __init__(
        self, files: Optional[list[FileInfo]] = None, total: int = 0, **kwargs
    ):
        self.files = files or []
        self.total = total
        super().__init__(**kwargs)


class DeleteResponse(BaseModel):
    def __init__(self, success: bool = False, message: str = "", **kwargs):
        self.success = success
        self.message = message
        super().__init__(**kwargs)


# Service Class


class UploadService:
    """Service for file upload and management."""

    @staticmethod
    def _generate_file_id() -> str:
        """Generate a unique file ID."""
        return str(uuid.uuid4())

    @staticmethod
    def _calculate_file_hash(file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash: {e}")
            return ""

    @staticmethod
    def _is_allowed_file(filename: str) -> bool:
        """Check if file extension is allowed."""
        return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def _get_safe_filename(filename: str) -> str:
        """Generate a safe filename."""
        # Remove potentially dangerous characters
        safe_chars = (
            "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
        safe_filename = "".join(c for c in filename if c in safe_chars)
        return safe_filename[:255]  # Limit filename length

    @staticmethod
    async def upload_file(file: UploadFile) -> UploadResponse:
        """Upload a file to the server."""
        try:
            if not file.filename:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "No file provided")

            # Check file extension
            if not UploadService._is_allowed_file(file.filename):
                raise HTTPException(
                    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    f"File type not allowed. Allowed types: {
                        ', '.join(ALLOWED_EXTENSIONS)
                    }",
                )

            # Read file content
            content = await file.read()

            # Check file size
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    f"File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024):.1f}MB",
                )

            # Generate unique file ID and safe filename
            file_id = UploadService._generate_file_id()
            safe_filename = UploadService._get_safe_filename(file.filename)
            stored_filename = f"{file_id}_{safe_filename}"
            file_path = UPLOAD_DIR / stored_filename

            # Save file
            with open(file_path, "wb") as f:
                f.write(content)

            # Calculate file hash
            file_hash = UploadService._calculate_file_hash(file_path)

            # Determine content type
            content_type = (
                file.content_type
                or mimetypes.guess_type(file.filename)[0]
                or "application/octet-stream"
            )

            # Create file info
            file_info = FileInfo(
                file_id=file_id,
                filename=stored_filename,
                original_filename=file.filename,
                content_type=content_type,
                size=len(content),
                file_hash=file_hash,
            )

            logger.info(
                f"File uploaded successfully: {
                    file.filename} -> {stored_filename}"
            )

            return UploadResponse(
                success=True, message="File uploaded successfully", file_info=file_info
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to upload file"
            )

    @staticmethod
    def get_file_info(file_id: str) -> FileInfo:
        """Get information about an uploaded file."""
        try:
            # Find file by ID
            for file_path in UPLOAD_DIR.glob(f"{file_id}_*"):
                if file_path.is_file():
                    stat = file_path.stat()
                    content_type = (
                        mimetypes.guess_type(str(file_path))[0]
                        or "application/octet-stream"
                    )

                    # Extract original filename
                    stored_filename = file_path.name
                    original_filename = stored_filename[
                        len(file_id) + 1 :
                    ]  # Remove file_id prefix

                    return FileInfo(
                        file_id=file_id,
                        filename=stored_filename,
                        original_filename=original_filename,
                        content_type=content_type,
                        size=stat.st_size,
                        upload_date=datetime.fromtimestamp(stat.st_ctime),
                        file_hash=UploadService._calculate_file_hash(file_path),
                    )

            raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to get file info"
            )

    @staticmethod
    def list_files(limit: int = 100, offset: int = 0) -> FileListResponse:
        """List uploaded files."""
        try:
            files = []
            all_files = list(UPLOAD_DIR.glob("*"))
            all_files.sort(key=lambda x: x.stat().st_ctime, reverse=True)

            for file_path in all_files[offset : offset + limit]:
                if file_path.is_file():
                    try:
                        # Extract file ID from filename
                        filename = file_path.name
                        if "_" in filename:
                            file_id = filename.split("_", 1)[0]
                            original_filename = filename.split("_", 1)[1]
                        else:
                            file_id = filename
                            original_filename = filename

                        stat = file_path.stat()
                        content_type = (
                            mimetypes.guess_type(str(file_path))[0]
                            or "application/octet-stream"
                        )

                        file_info = FileInfo(
                            file_id=file_id,
                            filename=filename,
                            original_filename=original_filename,
                            content_type=content_type,
                            size=stat.st_size,
                            upload_date=datetime.fromtimestamp(stat.st_ctime),
                        )
                        files.append(file_info)
                    except Exception as e:
                        logger.warning(f"Error processing file {file_path}: {e}")
                        continue

            return FileListResponse(files=files, total=len(all_files))

        except Exception as e:
            logger.error(f"Error listing files: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to list files"
            )

    @staticmethod
    def delete_file(file_id: str) -> DeleteResponse:
        """Delete an uploaded file."""
        try:
            # Find and delete file by ID
            deleted = False
            for file_path in UPLOAD_DIR.glob(f"{file_id}_*"):
                if file_path.is_file():
                    file_path.unlink()
                    deleted = True
                    logger.info(f"File deleted: {file_path.name}")
                    break

            if not deleted:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")

            return DeleteResponse(success=True, message="File deleted successfully")

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete file"
            )

    @staticmethod
    def get_file_path(file_id: str) -> Path:
        """Get the file path for a given file ID."""
        for file_path in UPLOAD_DIR.glob(f"{file_id}_*"):
            if file_path.is_file():
                return file_path
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")


# API Router
router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile):
    """Upload a file to the server."""
    return await UploadService.upload_file(file)


@router.get("/files", response_model=FileListResponse)
def list_files(limit: int = 100, offset: int = 0):
    """List uploaded files with pagination."""
    return UploadService.list_files(limit, offset)


@router.get("/files/{file_id}", response_model=FileInfo)
def get_file_info(file_id: str):
    """Get information about a specific file."""
    return UploadService.get_file_info(file_id)


@router.delete("/files/{file_id}", response_model=DeleteResponse)
def delete_file(file_id: str):
    """Delete a specific file."""
    return UploadService.delete_file(file_id)


@router.get("/download/{file_id}")
def download_file(file_id: str):
    """Download a specific file."""
    try:
        file_path = UploadService.get_file_path(file_id)
        file_info = UploadService.get_file_info(file_id)

        # In a real FastAPI application, you would return a FileResponse
        # For now, we'll return file information
        return {
            "file_path": str(file_path),
            "filename": file_info.original_filename,
            "content_type": file_info.content_type,
            "size": file_info.size,
        }
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to download file"
        )


@router.get("/health")
def health_check():
    """Health check endpoint for Upload service."""
    return {"status": "healthy", "service": "upload"}
