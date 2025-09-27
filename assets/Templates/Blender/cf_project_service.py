"""
Project service for managing video projects.
"""
import logging
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.backend.domain.models import Project, ProjectStatus, User, Channel

logger = logging.getLogger(__name__)


class ProjectService:
    """Service for managing video projects."""
    
    @staticmethod
    async def create_project(
        session: AsyncSession,
        title: str,
        description: Optional[str],
        owner_id: UUID,
        channel_id: Optional[UUID] = None,
        target_keywords: Optional[str] = None,
        target_audience: Optional[str] = None
    ) -> Optional[Project]:
        """Create a new project."""
        try:
            # Verify owner exists
            owner_result = await session.execute(select(User).where(User.id == owner_id))
            owner = owner_result.scalar_one_or_none()
            if not owner:
                logger.error(f"Owner with ID {owner_id} not found")
                return None
            
            # Verify channel exists and belongs to owner if provided
            if channel_id:
                channel_result = await session.execute(
                    select(Channel).where(
                        and_(Channel.id == channel_id, Channel.owner_id == owner_id)
                    )
                )
                channel = channel_result.scalar_one_or_none()
                if not channel:
                    logger.error(f"Channel with ID {channel_id} not found or doesn't belong to owner")
                    return None
            
            # Create new project
            project = Project(
                title=title,
                description=description,
                status=ProjectStatus.DRAFT,
                target_keywords=target_keywords,
                target_audience=target_audience,
                owner_id=owner_id,
                channel_id=channel_id
            )
            
            session.add(project)
            await session.commit()
            await session.refresh(project)
            
            logger.info(f"Created new project: {title} for user {owner_id}")
            return project
            
        except Exception as e:
            logger.error(f"Error creating project {title}: {e}")
            await session.rollback()
            return None
    
    @staticmethod
    async def get_project_by_id(session: AsyncSession, project_id: UUID, owner_id: UUID) -> Optional[Project]:
        """Get project by ID, ensuring it belongs to the owner."""
        try:
            result = await session.execute(
                select(Project)
                .options(selectinload(Project.channel))
                .where(and_(Project.id == project_id, Project.owner_id == owner_id))
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching project {project_id}: {e}")
            return None
    
    @staticmethod
    async def get_projects_by_owner(session: AsyncSession, owner_id: UUID) -> List[Project]:
        """Get all projects for a specific owner."""
        try:
            result = await session.execute(
                select(Project)
                .options(selectinload(Project.channel))
                .where(Project.owner_id == owner_id)
                .order_by(Project.created_at.desc())
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error fetching projects for owner {owner_id}: {e}")
            return []
    
    @staticmethod
    async def update_project(
        session: AsyncSession,
        project_id: UUID,
        owner_id: UUID,
        updates: Dict[str, Any]
    ) -> Optional[Project]:
        """Update a project."""
        try:
            # Get the project
            project = await ProjectService.get_project_by_id(session, project_id, owner_id)
            if not project:
                return None
            
            # Update allowed fields
            allowed_fields = {
                'title', 'description', 'status', 'target_keywords', 
                'target_audience', 'estimated_views', 'estimated_revenue', 'channel_id'
            }
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(project, field):
                    # Validate status if being updated
                    if field == 'status' and value not in [status.value for status in ProjectStatus]:
                        logger.error(f"Invalid status: {value}")
                        continue
                    
                    # Verify channel ownership if channel_id is being updated
                    if field == 'channel_id' and value is not None:
                        channel_result = await session.execute(
                            select(Channel).where(
                                and_(Channel.id == value, Channel.owner_id == owner_id)
                            )
                        )
                        channel = channel_result.scalar_one_or_none()
                        if not channel:
                            logger.error(f"Channel with ID {value} not found or doesn't belong to owner")
                            continue
                    
                    setattr(project, field, value)
            
            await session.commit()
            await session.refresh(project)
            
            logger.info(f"Updated project {project_id}")
            return project
            
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {e}")
            await session.rollback()
            return None
    
    @staticmethod
    async def delete_project(session: AsyncSession, project_id: UUID, owner_id: UUID) -> bool:
        """Delete a project."""
        try:
            # Get the project
            project = await ProjectService.get_project_by_id(session, project_id, owner_id)
            if not project:
                return False
            
            await session.delete(project)
            await session.commit()
            
            logger.info(f"Deleted project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {e}")
            await session.rollback()
            return False
    
    @staticmethod
    async def get_projects_by_status(
        session: AsyncSession, 
        owner_id: UUID, 
        status: ProjectStatus
    ) -> List[Project]:
        """Get projects by status for a specific owner."""
        try:
            result = await session.execute(
                select(Project)
                .options(selectinload(Project.channel))
                .where(and_(Project.owner_id == owner_id, Project.status == status.value))
                .order_by(Project.created_at.desc())
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error fetching projects by status {status} for owner {owner_id}: {e}")
            return []
    
    @staticmethod
    async def get_projects_by_channel(
        session: AsyncSession, 
        owner_id: UUID, 
        channel_id: UUID
    ) -> List[Project]:
        """Get projects for a specific channel."""
        try:
            result = await session.execute(
                select(Project)
                .options(selectinload(Project.channel))
                .where(and_(
                    Project.owner_id == owner_id, 
                    Project.channel_id == channel_id
                ))
                .order_by(Project.created_at.desc())
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error fetching projects for channel {channel_id}: {e}")
            return []