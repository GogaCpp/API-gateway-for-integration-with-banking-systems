from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional


class Document(BaseModel):
    id: uuid.UUID
    name: str
    discription: str
    path: str


class DocumentCreatePayload(BaseModel):
    name: str
    discription: str
    path: str
    user_id: uuid.UUID


class DocumentUpdatePayload(BaseModel):
    name: Optional[str]
    discription: Optional[str]


class BaseDocument(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    id: uuid.UUID
    path: str
    name: str
    discription: str
    created_at: datetime
    user_id: uuid.UUID


class BaseDocumentList(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    document_list: list[BaseDocument | None]
