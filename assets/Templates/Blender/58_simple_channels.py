"""Simplified Channels API module."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/channels", tags=["channels"])


@router.get("/")
def get_channels():
    """Get all channels."""
    return [
        {"id": "1", "name": "General", "description": "General discussion"},
        {"id": "2", "name": "Development", "description": "Development topics"},
    ]


@router.post("/")
def create_channel(channel_data: dict[str, str]):
    """Create a new channel."""
    return {
        "id": "new",
        "name": channel_data.get("name", "New Channel"),
        "status": "created",
    }


@router.get("/{channel_id}")
def get_channel(channel_id: str):
    """Get a specific channel."""
    return {
        "id": channel_id,
        "name": f"Channel {channel_id}",
        "description": "Channel description",
    }


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "channels"}
