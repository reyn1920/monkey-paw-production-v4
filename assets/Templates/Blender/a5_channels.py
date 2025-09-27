"""
Channel API endpoints for managing YouTube channels.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.infrastructure.database import db_manager
from src.backend.domain.models import User
from src.backend.services.channel_service import ChannelService
from src.backend.api.auth import get_current_user

router = APIRouter(prefix="/channels", tags=["channels"])


# Pydantic models for request/response
class ChannelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    youtube_channel_id: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class ChannelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    youtube_channel_id: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    subscriber_count: Optional[int] = Field(None, ge=0)
    video_count: Optional[int] = Field(None, ge=0)
    view_count: Optional[int] = Field(None, ge=0)


class ChannelResponse(BaseModel):
    id: UUID
    name: str
    youtube_channel_id: Optional[str]
    description: Optional[str]
    subscriber_count: Optional[int]
    video_count: Optional[int]
    view_count: Optional[int]
    owner_id: UUID
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


@router.post("/", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(
    channel_data: ChannelCreate,
    session: AsyncSession = Depends(db_manager.get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new channel."""
    channel = await ChannelService.create_channel(
        session=session,
        name=channel_data.name,
        owner_id=UUID(str(current_user.id)),
        youtube_channel_id=channel_data.youtube_channel_id,
        description=channel_data.description
    )
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create channel. YouTube channel ID may already exist."
        )
    
    return ChannelResponse(
        id=channel.id,
        name=str(channel.name),
        youtube_channel_id=str(channel.youtube_channel_id) if channel.youtube_channel_id is not None else None,
        description=str(channel.description) if channel.description is not None else None,
        subscriber_count=int(channel.subscriber_count) if channel.subscriber_count is not None else None,
        video_count=int(channel.video_count) if channel.video_count is not None else None,
        view_count=int(channel.view_count) if channel.view_count is not None else None,
        owner_id=channel.owner_id,
        created_at=channel.created_at.isoformat(),
        updated_at=channel.updated_at.isoformat()
    )


@router.get("/", response_model=List[ChannelResponse])
async def get_channels(
    session: AsyncSession = Depends(db_manager.get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all channels for the current user."""
    channels = await ChannelService.get_channels_by_owner(
        session, UUID(str(current_user.id))
    )
    
    return [
        ChannelResponse(
            id=channel.id,
            name=str(channel.name),
            youtube_channel_id=str(channel.youtube_channel_id) if channel.youtube_channel_id is not None else None,
            description=str(channel.description) if channel.description is not None else None,
            subscriber_count=int(channel.subscriber_count) if channel.subscriber_count is not None else None,
            video_count=int(channel.video_count) if channel.video_count is not None else None,
            view_count=int(channel.view_count) if channel.view_count is not None else None,
            owner_id=channel.owner_id,
            created_at=channel.created_at.isoformat(),
            updated_at=channel.updated_at.isoformat()
        )
        for channel in channels
    ]


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: UUID,
    session: AsyncSession = Depends(db_manager.get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific channel by ID."""
    channel = await ChannelService.get_channel_by_id(
        session, channel_id, UUID(str(current_user.id))
    )
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return ChannelResponse(
        id=channel.id,
        name=str(channel.name),
        youtube_channel_id=str(channel.youtube_channel_id) if channel.youtube_channel_id is not None else None,
        description=str(channel.description) if channel.description is not None else None,
        subscriber_count=int(channel.subscriber_count) if channel.subscriber_count is not None else None,
        video_count=int(channel.video_count) if channel.video_count is not None else None,
        view_count=int(channel.view_count) if channel.view_count is not None else None,
        owner_id=channel.owner_id,
        created_at=channel.created_at.isoformat(),
        updated_at=channel.updated_at.isoformat()
    )


@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: UUID,
    channel_data: ChannelUpdate,
    session: AsyncSession = Depends(db_manager.get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a channel."""
    # Convert Pydantic model to dict, excluding None values
    updates = {k: v for k, v in channel_data.model_dump().items() if v is not None}
    
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update"
        )
    
    channel = await ChannelService.update_channel(
        session, channel_id, UUID(str(current_user.id)), updates
    )
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found or update failed"
        )
    
    return ChannelResponse(
        id=channel.id,
        name=str(channel.name),
        youtube_channel_id=str(channel.youtube_channel_id) if channel.youtube_channel_id is not None else None,
        description=str(channel.description) if channel.description is not None else None,
        subscriber_count=int(channel.subscriber_count) if channel.subscriber_count is not None else None,
        video_count=int(channel.video_count) if channel.video_count is not None else None,
        view_count=int(channel.view_count) if channel.view_count is not None else None,
        owner_id=channel.owner_id,
        created_at=channel.created_at.isoformat(),
        updated_at=channel.updated_at.isoformat()
    )


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: UUID,
    session: AsyncSession = Depends(db_manager.get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a channel."""
    success = await ChannelService.delete_channel(
        session, channel_id, UUID(str(current_user.id))
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )


@router.get("/youtube/{youtube_channel_id}", response_model=ChannelResponse)
async def get_channel_by_youtube_id(
    youtube_channel_id: str,
    session: AsyncSession = Depends(db_manager.get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a channel by YouTube channel ID."""
    channel = await ChannelService.get_channel_by_youtube_id(
        session, youtube_channel_id, UUID(str(current_user.id))
    )
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return ChannelResponse(
        id=channel.id,
        name=str(channel.name),
        youtube_channel_id=str(channel.youtube_channel_id) if channel.youtube_channel_id is not None else None,
        description=str(channel.description) if channel.description is not None else None,
        subscriber_count=int(channel.subscriber_count) if channel.subscriber_count is not None else None,
        video_count=int(channel.video_count) if channel.video_count is not None else None,
        view_count=int(channel.view_count) if channel.view_count is not None else None,
        owner_id=channel.owner_id,
        created_at=channel.created_at.isoformat(),
        updated_at=channel.updated_at.isoformat()
    )


@router.patch("/{channel_id}/stats", response_model=ChannelResponse)
async def update_channel_stats(
    channel_id: UUID,
    subscriber_count: int = Query(..., ge=0),
    video_count: int = Query(..., ge=0),
    view_count: int = Query(..., ge=0),
    session: AsyncSession = Depends(db_manager.get_session),
    current_user: User = Depends(get_current_user)
):
    """Update channel statistics."""
    channel = await ChannelService.update_channel_stats(
        session, channel_id, UUID(str(current_user.id)),
        subscriber_count, video_count, view_count
    )
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return ChannelResponse(
        id=channel.id,
        name=str(channel.name),
        youtube_channel_id=str(channel.youtube_channel_id) if channel.youtube_channel_id is not None else None,
        description=str(channel.description) if channel.description is not None else None,
        subscriber_count=int(channel.subscriber_count) if channel.subscriber_count is not None else None,
        video_count=int(channel.video_count) if channel.video_count is not None else None,
        view_count=int(channel.view_count) if channel.view_count is not None else None,
        owner_id=channel.owner_id,
        created_at=channel.created_at.isoformat(),
        updated_at=channel.updated_at.isoformat()
    )