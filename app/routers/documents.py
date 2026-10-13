from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.controllers.documents_controller import DocumentsController
from app.dependencies import get_documents_controller
from app.schemas.documents import (
    DocumentCreateRequest,
    DocumentResponse,
    DocumentUpdateRequest,
)
from app.schemas.errors import ErrorResponse

router = APIRouter(prefix="/documents", tags=["documents"])

ControllerDep = Annotated[DocumentsController, Depends(get_documents_controller)]

_NOT_FOUND = {404: {"model": ErrorResponse, "description": "Document not found"}}
_INVALID = {422: {"model": ErrorResponse, "description": "Validation failed"}}


@router.post("", response_model=DocumentResponse, responses=_INVALID,
             status_code=status.HTTP_201_CREATED, summary="Create a document")
async def create_document(payload: DocumentCreateRequest, controller: ControllerDep) -> DocumentResponse:
    return await controller.create(payload)


@router.get("", response_model=list[DocumentResponse], summary="List documents")
async def list_documents(controller: ControllerDep) -> list[DocumentResponse]:
    return await controller.list_all()


@router.get("/{document_id}", response_model=DocumentResponse, responses=_NOT_FOUND,
            summary="Get a document")
async def get_document(document_id: str, controller: ControllerDep) -> DocumentResponse:
    return await controller.get(document_id)


@router.put("/{document_id}", response_model=DocumentResponse,
            responses={**_NOT_FOUND, **_INVALID}, summary="Replace a document")
async def replace_document(document_id: str, payload: DocumentUpdateRequest,
                           controller: ControllerDep) -> DocumentResponse:
    return await controller.replace(document_id, payload)


@router.delete("/{document_id}", responses=_NOT_FOUND,
               status_code=status.HTTP_204_NO_CONTENT, summary="Delete a document")
async def delete_document(document_id: str, controller: ControllerDep) -> None:
    await controller.delete(document_id)