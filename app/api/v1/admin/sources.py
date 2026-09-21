import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.source import SourceCreate, SourceResponse
from app.services.source_service import SourceService


router = APIRouter(
    prefix="/admin/sources",
    tags=["Admin - Sources"],
)

service = SourceService()


@router.post(
    "",
    response_model=SourceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_source(
    data: SourceCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return service.create_source(
        db,
        data,
    )


@router.get(
    "",
    response_model=list[SourceResponse],
)
def get_sources(
    db: Annotated[Session, Depends(get_db)],
):
    return service.get_sources(db)


@router.get(
    "/{source_id}",
    response_model=SourceResponse,
)
def get_source(
    source_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    return service.get_source(
        db,
        source_id,
    )