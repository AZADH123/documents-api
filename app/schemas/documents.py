from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------- requests ----------

class DocumentCreateRequest(BaseModel):
    """POST body. extra='forbid' rejects unknown fields (Pydantic's .strict())."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200, examples=["Quarterly report"])
    content: str


class DocumentUpdateRequest(DocumentCreateRequest):
    """PUT body — full replacement, so both fields required."""


# ---------- responses ----------

class DocumentResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    content: str
    created_at: datetime = Field(alias="createdAt")   # camelCase on the wire