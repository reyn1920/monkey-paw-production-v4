"""
Channel service for managing YouTube channels.
"""
import logging
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.backend.domain.models import Channel, User

logger = logging.getLogger(__name__)


class ChannelService:
    """Service for managing YouTube channels."""
    
    @staticmethod
    async def create_channel(
        session: AsyncSession,
        name: str,
        owner_id: UUID,
        youtube_channel_id: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Channel]:
        """Create a new channel."""
        try:
            # Verify owner exists
            owner_result = await session.execute(select(User).where(User.id == owner_id))
            owner = owner_result.scalar_one_or_none()
            if not owner:
                logger.error(f"Owner with ID {owner_id} not found")
                return None
            
            # Check if YouTube channel ID is already taken (if provided)
            if youtube_channel_id:
                existing_channel = await session.execute(
                    select(Channel).where(Channel.youtube_channel_id == youtube_channel_id)
                )
                if existing_channel.scalar_one_or_none():
                    logger.error(f"YouTube channel ID {youtube_channel_id} already exists")
                    return None
            
            # Create new channel
            channel = Channel(
                name=name,
                youtube_channel_id=youtube_channel_id,
                description=description,
                owner_id=owner_id
            )
            
            session.add(channel)
            await session.commit()
            await session.refresh(channel)
            
            logger.info(f"Created new channel: {name} for user {owner_id}")
            return channel
            
        except Exception as e:
            logger.error(f"Error creating channel {name}: {e}")
            await session.rollback()
            return None
    
    @staticmethod
    async def get_channel_by_id(session: AsyncSession, channel_id: UUID, owner_id: UUID) -> Optional[Channel]:
        """Get channel by ID, ensuring it belongs to the owner."""
        try:
            result = await session.execute(
                select(Channel)
                .options(selectinload(Channel.projects))
                .where(and_(Channel.id == channel_id, Channel.owner_id == owner_id))
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching channel {channel_id}: {e}")
            return None
    
    @staticmethod
    async def get_channels_by_owner(session: AsyncSession, owner_id: UUID) -> List[Channel]:
        """Get all channels for a specific owner."""
        try:
            result = await session.execute(
                select(Channel)
                .options(selectinload(Channel.projects))
                .where(Channel.owner_id == owner_id)
                .order_by(Channel.created_at.desc())
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error fetching channels for owner {owner_id}: {e}")
            return []
    
    @staticmethod
    async def update_channel(
        session: AsyncSession,
        channel_id: UUID,
        owner_id: UUID,
        updates: Dict[str, Any]
    ) -> Optional[Channel]:
        """Update a channel."""
        try:
            # Get the channel
            channel = await ChannelService.get_channel_by_id(session, channel_id, owner_id)
            if not channel:
                return None
            
            # Update allowed fields
            allowed_fields = {
                'name', 'youtube_channel_id', 'description', 
                'subscriber_count', 'video_count', 'view_count'
            }
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(channel, field):
                    # Check for duplicate YouTube channel ID if being updated
                    if field == 'youtube_channel_id' and value is not None:
                        existing_channel = await session.execute(
                            select(Channel).where(
                                and_(
                                    Channel.youtube_channel_id == value,
                                    Channel.id != channel_id
                                )
                            )
                        )
                        if existing_channel.scalar_one_or_none():
                            logger.error(f"YouTube channel ID {value} already exists")
                            continue
                    
                    setattr(channel, field, value)
            
            await session.commit()
            await session.refresh(channel)
            
            logger.info(f"Updated channel {channel_id}")
            return channel
            
        except Exception as e:
            logger.error(f"Error updating channel {channel_id}: {e}")
            await session.rollback()
            return None
    
    @staticmethod
    async def delete_channel(session: AsyncSession, channel_id: UUID, owner_id: UUID) -> bool:
        """Delete a channel."""
        try:
            # Get the channel
            channel = await ChannelService.get_channel_by_id(session, channel_id, owner_id)
            if not channel:
                return False
            
            await session.delete(channel)
            await session.commit()
            
            logger.info(f"Deleted channel {channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting channel {channel_id}: {e}")
            await session.rollback()
            return False
    
    @staticmethod
    async def get_channel_by_youtube_id(
        session: AsyncSession, 
        youtube_channel_id: str, 
        owner_id: UUID
    ) -> Optional[Channel]:
        """Get channel by YouTube channel ID for a specific owner."""
        try:
            result = await session.execute(
                select(Channel)
                .options(selectinload(Channel.projects))
                .where(and_(
                    Channel.youtube_channel_id == youtube_channel_id,
                    Channel.owner_id == owner_id
                ))
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching channel by YouTube ID {youtube_channel_id}: {e}")
            return None
    
    @staticmethod
    async def update_channel_stats(
        session: AsyncSession,
        channel_id: UUID,
        owner_id: UUID,
        subscriber_count: int,
        video_count: int,
        view_count: int
    ) -> Optional[Channel]:
        """Update channel statistics."""
        try:
            updates = {
                'subscriber_count': subscriber_count,
                'video_count': video_count,
                'view_count': view_count
            }
            
            return await ChannelService.update_channel(
                session, channel_id, owner_id, updates
            )
            
        except Exception as e:
            logger.error(f"Error updating channel stats for {channel_id}: {e}")
            return None