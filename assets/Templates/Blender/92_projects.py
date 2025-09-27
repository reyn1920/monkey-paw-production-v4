"""Project API endpoints."""
import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.infrastructure.database import db_manager
from src.backend.services.project_service import ProjectService
from src.backend.domain.models import User, ProjectStatus
from src.backend.api.auth import get_current_user

logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/projects", tags=["projects"])


# Pydantic models
class ProjectCreate(BaseModel):
    """Project creation model."""
    title: str = Field(..., min_length=1, max_length=255, description="Project title")
    description: Optional[str] = Field(None, max_length=1000, description="Project description")
    channel_id: Optional[UUID] = Field(None, description="Associated channel ID")
    target_keywords: Optional[str] = Field(None, max_length=500, description="Target keywords")
    target_audience: Optional[str] = Field(None, max_length=255, description="Target audience")


class ProjectUpdate(BaseModel):
    """Project update model."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Project title")
    description: Optional[str] = Field(None, max_length=1000, description="Project description")
    status: Optional[ProjectStatus] = Field(None, description="Project status")
    channel_id: Optional[UUID] = Field(None, description="Associated channel ID")
    target_keywords: Optional[str] = Field(None, max_length=500, description="Target keywords")
    target_audience: Optional[str] = Field(None, max_length=255, description="Target audience")
    estimated_views: Optional[int] = Field(None, ge=0, description="Estimated views")
    estimated_revenue: Optional[float] = Field(None, ge=0.0, description="Estimated revenue")


class ProjectResponse(BaseModel):
    """Project response model."""
    id: str
    title: str
    description: Optional[str]
    status: str
    target_keywords: Optional[str]
    target_audience: Optional[str]
    estimated_views: int
    estimated_revenue: float
    owner_id: str
    channel_id: Optional[str]
    created_at: str
    updated_at: str
    channel_name: Optional[str] = None


# API endpoints
@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_manager.get_session)
) -> ProjectResponse:
    """Create a new project."""
    try:
        project = await ProjectService.create_project(
            session=session,
            title=project_data.title,
            description=project_data.description,
            owner_id=UUID(str(current_user.id)),
            channel_id=project_data.channel_id,
            target_keywords=project_data.target_keywords,
            target_audience=project_data.target_audience
        )
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create project"
            )
        
        return ProjectResponse(
            id=str(project.id),
            title=str(project.title),
            description=str(project.description) if project.description is not None else None,
            status=str(project.status),
            target_keywords=str(project.target_keywords) if project.target_keywords is not None else None,
            target_audience=str(project.target_audience) if project.target_audience is not None else None,
            estimated_views=int(project.estimated_views),
            estimated_revenue=float(project.estimated_revenue),
            owner_id=str(project.owner_id),
            channel_id=str(project.channel_id) if project.channel_id is not None else None,
            created_at=project.created_at.isoformat(),
            updated_at=project.updated_at.isoformat(),
            channel_name=str(project.channel.name) if project.channel is not None else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    status_filter: Optional[ProjectStatus] = Query(None, description="Filter by project status"),
    channel_id: Optional[UUID] = Query(None, description="Filter by channel ID"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_manager.get_session)
) -> List[ProjectResponse]:
    """Get all projects for the current user with optional filters."""
    try:
        if status_filter:
            projects = await ProjectService.get_projects_by_status(
                session, UUID(str(current_user.id)), status_filter
            )
        elif channel_id:
            projects = await ProjectService.get_projects_by_channel(
                session, UUID(str(current_user.id)), channel_id
            )
        else:
            projects = await ProjectService.get_projects_by_owner(
                session, UUID(str(current_user.id))
            )
        
        return [
            ProjectResponse(
                id=str(project.id),
                title=str(project.title),
                description=str(project.description) if project.description else None,
                status=str(project.status),
                target_keywords=str(project.target_keywords) if project.target_keywords else None,
                target_audience=str(project.target_audience) if project.target_audience else None,
                estimated_views=int(project.estimated_views),
                estimated_revenue=float(project.estimated_revenue),
                owner_id=str(project.owner_id),
                channel_id=str(project.channel_id) if project.channel_id else None,
                created_at=project.created_at.isoformat(),
                updated_at=project.updated_at.isoformat(),
                channel_name=str(project.channel.name) if project.channel else None
            )
            for project in projects
        ]
        
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_manager.get_session)
) -> ProjectResponse:
    """Get a specific project by ID."""
    try:
        project = await ProjectService.get_project_by_id(
            session, project_id, current_user.id
        )
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return ProjectResponse(
            id=str(project.id),
            title=str(project.title),
            description=str(project.description) if project.description else None,
            status=str(project.status),
            target_keywords=str(project.target_keywords) if project.target_keywords else None,
            target_audience=str(project.target_audience) if project.target_audience else None,
            estimated_views=int(project.estimated_views),
            estimated_revenue=float(project.estimated_revenue),
            owner_id=str(project.owner_id),
            channel_id=str(project.channel_id) if project.channel_id else None,
            created_at=project.created_at.isoformat(),
            updated_at=project.updated_at.isoformat(),
            channel_name=str(project.channel.name) if project.channel else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_manager.get_session)
) -> ProjectResponse:
    """Update a project."""
    try:
        # Convert Pydantic model to dict, excluding None values
        updates = project_data.model_dump(exclude_none=True)
        
        project = await ProjectService.update_project(
            session, project_id, current_user.id, updates
        )
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return ProjectResponse(
            id=str(project.id),
            title=str(project.title),
            description=str(project.description) if project.description else None,
            status=str(project.status),
            target_keywords=str(project.target_keywords) if project.target_keywords else None,
            target_audience=str(project.target_audience) if project.target_audience else None,
            estimated_views=int(project.estimated_views),
            estimated_revenue=float(project.estimated_revenue),
            owner_id=str(project.owner_id),
            channel_id=str(project.channel_id) if project.channel_id else None,
            created_at=project.created_at.isoformat(),
            updated_at=project.updated_at.isoformat(),
            channel_name=str(project.channel.name) if project.channel else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_manager.get_session)
) -> None:
    """Delete a project."""
    try:
        success = await ProjectService.delete_project(
            session, project_id, current_user.id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )