"""Library API endpoints for managing library resources and collections."""

from typing import Optional, Any
from datetime import datetime
import uuid
import logging

# Simple fallback classes for missing dependencies
try:
    from fastapi import APIRouter, HTTPException, Query, Path
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback classes if FastAPI is not available
    class APIRouter:
        def __init__(self, **kwargs):
            self.routes = []
            self.prefix = kwargs.get("prefix", "")
            self.tags = kwargs.get("tags", [])

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

        def put(self, path: str, **kwargs):
            def decorator(func):
                self.routes.append({"method": "PUT", "path": path, "func": func})
                return func

            return decorator

        def delete(self, path: str, **kwargs):
            def decorator(func):
                self.routes.append({"method": "DELETE", "path": path, "func": func})
                return func

            return decorator

    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail

    def Field(**kwargs):
        return None

    def Query(**kwargs):
        return None

    def Path(**kwargs):
        return None


# Configure logging
logger = logging.getLogger(__name__)


# Pydantic Models
class LibraryItemBase(BaseModel):
    title: str = Field(..., description="Title of the library item")
    author: Optional[str] = Field(None, description="Author of the item")
    category: str = Field(..., description="Category of the item")
    description: Optional[str] = Field(None, description="Description of the item")
    tags: list[str] = Field(
        default_factory=list, description="Tags associated with the item"
    )


class LibraryItemCreate(LibraryItemBase):
    pass


class LibraryItemUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the library item")
    author: Optional[str] = Field(None, description="Author of the item")
    category: Optional[str] = Field(None, description="Category of the item")
    description: Optional[str] = Field(None, description="Description of the item")
    tags: Optional[list[str]] = Field(None, description="Tags associated with the item")


class LibraryItemResponse(LibraryItemBase):
    id: str = Field(..., description="Unique identifier for the library item")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    status: str = Field(default="active", description="Status of the item")


class LibraryCollectionBase(BaseModel):
    name: str = Field(..., description="Name of the collection")
    description: Optional[str] = Field(
        None, description="Description of the collection"
    )
    is_public: bool = Field(
        default=True, description="Whether the collection is public"
    )


class LibraryCollectionCreate(LibraryCollectionBase):
    pass


class LibraryCollectionResponse(LibraryCollectionBase):
    id: str = Field(..., description="Unique identifier for the collection")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    item_count: int = Field(default=0, description="Number of items in the collection")


# In-memory storage (replace with database in production)
library_items: dict[str, dict[str, Any]] = {}
library_collections: dict[str, dict[str, Any]] = {}
# collection_id -> list of item_ids
collection_items: dict[str, list[str]] = {}


# Service Classes
class LibraryService:
    """Service for managing library items and collections."""

    @staticmethod
    def create_item(item_data: LibraryItemCreate) -> LibraryItemResponse:
        """Create a new library item."""
        item_id = str(uuid.uuid4())
        now = datetime.utcnow()

        item = {
            "id": item_id,
            "title": item_data.title,
            "author": item_data.author,
            "category": item_data.category,
            "description": item_data.description,
            "tags": item_data.tags,
            "created_at": now,
            "updated_at": now,
            "status": "active",
        }

        library_items[item_id] = item
        logger.info(f"Created library item: {item_id}")

        return LibraryItemResponse(**item)

    @staticmethod
    def get_items(
        category: Optional[str] = None, tag: Optional[str] = None
    ) -> list[LibraryItemResponse]:
        """Get all library items with optional filtering."""
        items = []

        for item in library_items.values():
            # Apply filters
            if category and item.get("category") != category:
                continue
            if tag and tag not in item.get("tags", []):
                continue

            items.append(LibraryItemResponse(**item))

        return sorted(items, key=lambda x: x.created_at, reverse=True)

    @staticmethod
    def get_item(item_id: str) -> LibraryItemResponse:
        """Get a specific library item."""
        if item_id not in library_items:
            raise HTTPException(status_code=404, detail="Library item not found")

        return LibraryItemResponse(**library_items[item_id])

    @staticmethod
    def update_item(item_id: str, item_data: LibraryItemUpdate) -> LibraryItemResponse:
        """Update a library item."""
        if item_id not in library_items:
            raise HTTPException(status_code=404, detail="Library item not found")

        item = library_items[item_id]
        update_data = item_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            item[field] = value

        item["updated_at"] = datetime.utcnow()
        logger.info(f"Updated library item: {item_id}")

        return LibraryItemResponse(**item)

    @staticmethod
    def delete_item(item_id: str) -> dict[str, str]:
        """Delete a library item."""
        if item_id not in library_items:
            raise HTTPException(status_code=404, detail="Library item not found")

        del library_items[item_id]

        # Remove from all collections
        for collection_id, items in collection_items.items():
            if item_id in items:
                items.remove(item_id)

        logger.info(f"Deleted library item: {item_id}")
        return {"message": "Library item deleted successfully"}

    @staticmethod
    def create_collection(
        collection_data: LibraryCollectionCreate,
    ) -> LibraryCollectionResponse:
        """Create a new library collection."""
        collection_id = str(uuid.uuid4())
        now = datetime.utcnow()

        collection = {
            "id": collection_id,
            "name": collection_data.name,
            "description": collection_data.description,
            "is_public": collection_data.is_public,
            "created_at": now,
            "updated_at": now,
            "item_count": 0,
        }

        library_collections[collection_id] = collection
        collection_items[collection_id] = []
        logger.info(f"Created library collection: {collection_id}")

        return LibraryCollectionResponse(**collection)

    @staticmethod
    def get_collections() -> list[LibraryCollectionResponse]:
        """Get all library collections."""
        collections = []

        for collection in library_collections.values():
            collection["item_count"] = len(collection_items.get(collection["id"], []))
            collections.append(LibraryCollectionResponse(**collection))

        return sorted(collections, key=lambda x: x.created_at, reverse=True)

    @staticmethod
    def add_item_to_collection(collection_id: str, item_id: str) -> dict[str, str]:
        """Add an item to a collection."""
        if collection_id not in library_collections:
            raise HTTPException(status_code=404, detail="Collection not found")

        if item_id not in library_items:
            raise HTTPException(status_code=404, detail="Library item not found")

        if collection_id not in collection_items:
            collection_items[collection_id] = []

        if item_id not in collection_items[collection_id]:
            collection_items[collection_id].append(item_id)
            library_collections[collection_id]["updated_at"] = datetime.utcnow()
            logger.info(f"Added item {item_id} to collection {collection_id}")

        return {"message": "Item added to collection successfully"}


# Initialize with some sample data
def init_sample_data():
    """Initialize with sample library data."""
    if not library_items:  # Only initialize if empty
        sample_items = [
            {
                "title": "FastAPI Best Practices",
                "author": "John Doe",
                "category": "Programming",
                "description": "A comprehensive guide to FastAPI development",
                "tags": ["python", "fastapi", "web-development"],
            },
            {
                "title": "Modern JavaScript Patterns",
                "author": "Jane Smith",
                "category": "Programming",
                "description": "Advanced JavaScript patterns and techniques",
                "tags": ["javascript", "patterns", "frontend"],
            },
            {
                "title": "Database Design Principles",
                "author": "Bob Johnson",
                "category": "Database",
                "description": "Fundamental principles of database design",
                "tags": ["database", "design", "sql"],
            },
        ]

        for item_data in sample_items:
            LibraryService.create_item(LibraryItemCreate(**item_data))

        # Create a sample collection
        collection = LibraryService.create_collection(
            LibraryCollectionCreate(
                name="Programming Resources",
                description="Essential programming books and guides",
                is_public=True,
            )
        )

        # Add items to collection
        for item_id in list(library_items.keys())[:2]:
            LibraryService.add_item_to_collection(collection.id, item_id)


# Initialize sample data
init_sample_data()

# API Router
router = APIRouter(prefix="/api/library", tags=["library"])


@router.post("/items", response_model=LibraryItemResponse)
def create_library_item(item: LibraryItemCreate):
    """Create a new library item."""
    return LibraryService.create_item(item)


@router.get("/items", response_model=list[LibraryItemResponse])
def get_library_items(
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
):
    """Get all library items with optional filtering."""
    return LibraryService.get_items(category=category, tag=tag)


@router.get("/items/{item_id}", response_model=LibraryItemResponse)
def get_library_item(item_id: str = Path(..., description="Library item ID")):
    """Get a specific library item."""
    return LibraryService.get_item(item_id)


@router.put("/items/{item_id}", response_model=LibraryItemResponse)
def update_library_item(
    item_id: str = Path(..., description="Library item ID"),
    item: LibraryItemUpdate = None,
):
    """Update a library item."""
    return LibraryService.update_item(item_id, item)


@router.delete("/items/{item_id}")
def delete_library_item(item_id: str = Path(..., description="Library item ID")):
    """Delete a library item."""
    return LibraryService.delete_item(item_id)


@router.post("/collections", response_model=LibraryCollectionResponse)
def create_library_collection(collection: LibraryCollectionCreate):
    """Create a new library collection."""
    return LibraryService.create_collection(collection)


@router.get("/collections", response_model=list[LibraryCollectionResponse])
def get_library_collections():
    """Get all library collections."""
    return LibraryService.get_collections()


@router.post("/collections/{collection_id}/items/{item_id}")
def add_item_to_collection(
    collection_id: str = Path(..., description="Collection ID"),
    item_id: str = Path(..., description="Library item ID"),
):
    """Add an item to a collection."""
    return LibraryService.add_item_to_collection(collection_id, item_id)


@router.get("/health")
def library_health_check():
    """Health check for library service."""
    return {
        "status": "healthy",
        "service": "library",
        "timestamp": datetime.utcnow().isoformat(),
        "items_count": len(library_items),
        "collections_count": len(library_collections),
    }
