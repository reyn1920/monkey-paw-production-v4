"""Simplified Pets API module."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/pets", tags=["pets"])


@router.get("/")
def get_pets():
    """Get all pets."""
    return [
        {"id": "1", "name": "Buddy", "type": "dog", "age": 3},
        {"id": "2", "name": "Whiskers", "type": "cat", "age": 2},
    ]


@router.post("/")
def create_pet(pet_data: dict[str, str]):
    """Create a new pet."""
    return {"id": "new", "name": pet_data.get("name", "New Pet"), "status": "created"}


@router.get("/{pet_id}")
def get_pet(pet_id: str):
    """Get a specific pet."""
    return {"id": pet_id, "name": f"Pet {pet_id}", "type": "unknown"}


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "pets"}
