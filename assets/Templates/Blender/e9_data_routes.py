"""
API routes for data operations.
"""

from typing import Dict, Any, List, Optional
import logging

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

# Import the actual DataService and QueryResult from the correct location
from src.services.data import DataService, QueryResult

logger = logging.getLogger(__name__)


# Pydantic models for request/response
class QueryRequest(BaseModel):
    """Request model for SQL queries."""

    query: str
    params: Optional[Dict[str, Any]] = None


class ExecuteRequest(BaseModel):
    """Request model for SQL execution."""

    query: str
    params: Optional[Dict[str, Any]] = None


class DataResponse(BaseModel):
    """Response model for data operations."""

    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    rows_affected: int = 0
    message: str = ""
    error: Optional[str] = None


# Global data service instance
data_service: Optional[DataService] = None


async def get_data_service() -> DataService:
    """Get or initialize the data service."""
    global data_service
    if data_service is None:
        data_service = DataService()
        await data_service.initialize()
    elif not data_service.is_initialized:
        await data_service.initialize()
    return data_service


# Create router
router = APIRouter(prefix="/api", tags=["data"])


@router.get("/data")
async def get_data(
    table: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    service: DataService = Depends(get_data_service),
):
    """Get data from the database."""
    try:
        if table:
            query = f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset}"
        else:
            # Return available tables
            query = "SELECT name FROM sqlite_master WHERE type='table'"

        result = await service.execute_query(query)

        if result.success:
            return DataResponse(
                success=True,
                data=result.data,
                rows_affected=len(result.data) if result.data else 0,
                message=f"Retrieved {len(result.data) if result.data else 0} rows",
            )
        else:
            return DataResponse(
                success=False, error=result.error, message="Failed to retrieve data"
            )
    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/query")
async def execute_query(
    request: QueryRequest, service: DataService = Depends(get_data_service)
):
    """Execute a custom SQL query."""
    try:
        # Basic SQL injection protection
        if any(
            dangerous in request.query.upper()
            for dangerous in ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        ):
            if not request.query.upper().startswith("SELECT"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only SELECT queries are allowed through this endpoint",
                )

        result = await service.execute_query(request.query, request.params)

        if result.success:
            return DataResponse(
                success=True,
                data=result.data,
                rows_affected=len(result.data) if result.data else 0,
                message=f"Query executed successfully, {len(result.data) if result.data else 0} rows returned",
            )
        else:
            return DataResponse(
                success=False, error=result.error, message="Query execution failed"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in execute_query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/execute")
async def execute_statement(
    request: ExecuteRequest, service: DataService = Depends(get_data_service)
):
    """Execute a SQL statement (INSERT, UPDATE, DELETE)."""
    try:
        # Allow only specific statement types
        allowed_statements = ["INSERT", "UPDATE", "DELETE", "CREATE", "ALTER"]
        query_upper = request.query.strip().upper()

        if not any(query_upper.startswith(stmt) for stmt in allowed_statements):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only INSERT, UPDATE, DELETE, CREATE, and ALTER statements are allowed",
            )

        result = await service.execute_query(request.query, request.params)

        if result.success:
            return DataResponse(
                success=True,
                rows_affected=result.rows_affected,
                message=f"Statement executed successfully, {result.rows_affected} rows affected",
            )
        else:
            return DataResponse(
                success=False, error=result.error, message="Statement execution failed"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in execute_statement: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Health check endpoint
@router.get("/data/health")
async def data_health_check(service: DataService = Depends(get_data_service)):
    """Check the health of the data service."""
    try:
        # Simple query to test connection
        result = await service.execute_query("SELECT 1 as test")

        if result.success:
            return {
                "status": "healthy",
                "database_path": service.database_path,
                "initialized": service.is_initialized,
            }
        else:
            return {"status": "unhealthy", "error": result.error}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}
