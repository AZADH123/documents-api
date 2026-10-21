"""
====================================================================
app/routers/documents.py — the documents route table (PROTECTED).
====================================================================

Every route here is now protected: the client must send a valid JWT
in the `Authorization: Bearer <token>` header. We enforce this by
adding `current_user: CurrentUser` to each route's signature —
FastAPI automatically runs `get_current_user` (which decodes the
JWT) before our handler runs. If the token is missing or invalid,
FastAPI short-circuits with a 401 response and our handler never runs.

We don't actually USE `current_user` inside the handlers (yet) —
its presence in the signature is what triggers the auth check.
Later you might use it for per-user document ownership.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.controllers.documents_controller import DocumentsController
from app.dependencies import get_current_user
from app.domain.entities import User
from app.schemas.documents import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)

router = APIRouter(prefix="/documents", tags=["documents"])

# Reusable type alias — any parameter annotated with this triggers
# the JWT verification flow.
CurrentUser = Annotated[User, Depends(get_current_user)]


# --------------------------------------------------------------------
# POST /documents/  -> create a new document
# --------------------------------------------------------------------
@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    current_user: CurrentUser,
    payload: DocumentCreate,
    controller: DocumentsController = Depends(),
) -> DocumentResponse:
    return controller.create(payload)


# --------------------------------------------------------------------
# GET /documents/  -> list all documents
# --------------------------------------------------------------------
@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    current_user: CurrentUser,
    controller: DocumentsController = Depends(),
) -> list[DocumentResponse]:
    return controller.list_all()


# --------------------------------------------------------------------
# GET /documents/{document_id}  -> get one document
# --------------------------------------------------------------------
@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    current_user: CurrentUser,
    document_id: str,
    controller: DocumentsController = Depends(),
) -> DocumentResponse:
    return controller.get(document_id)


# --------------------------------------------------------------------
# PUT /documents/{document_id}  -> update an existing document
# --------------------------------------------------------------------
@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    current_user: CurrentUser,
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
    current_user: CurrentUser,
    document_id: str,
    controller: DocumentsController = Depends(),
) -> None:
    controller.delete(document_id)