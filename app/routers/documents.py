"""
====================================================================
app/routers/documents.py — the documents route table.
====================================================================

A "router" is just a collection of endpoints grouped under a
common prefix. This file declares the 5 CRUD endpoints for
documents and wires each one to a method on the controller.

The router itself contains NO logic — it only describes the
HTTP surface (path, method, status code, request/response schema)
and delegates to the controller.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.documents_controller import DocumentsController
from app.schemas.documents import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)

# All routes here are prefixed with /documents and tagged "documents"
# (the tag groups them in the /docs UI).
router = APIRouter(prefix="/documents", tags=["documents"])


# --------------------------------------------------------------------
# POST /documents/  -> create a new document
# --------------------------------------------------------------------
@router.post("/",response_model=DocumentResponse,status_code=status.HTTP_201_CREATED,)
def create_document(payload: DocumentCreate,controller: DocumentsController = Depends(),) -> DocumentResponse:
    return controller.create(payload)


# --------------------------------------------------------------------
# GET /documents/  -> list all documents
# --------------------------------------------------------------------
@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    controller: DocumentsController = Depends(),
) -> list[DocumentResponse]:
    return controller.list_all()


# --------------------------------------------------------------------
# GET /documents/{document_id}  -> get one document
# --------------------------------------------------------------------
@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    controller: DocumentsController = Depends(),
) -> DocumentResponse:
    return controller.get(document_id)


# --------------------------------------------------------------------
# PUT /documents/{document_id}  -> update an existing document
# --------------------------------------------------------------------
@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: str,
    payload: DocumentUpdate,
    controller: DocumentsController = Depends(),
) -> DocumentResponse:
    return controller.update(document_id, payload)


# --------------------------------------------------------------------
# DELETE /documents/{document_id}  -> delete an existing document
# --------------------------------------------------------------------
@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str,
    controller: DocumentsController = Depends(),
) -> None:
    controller.delete(document_id)
