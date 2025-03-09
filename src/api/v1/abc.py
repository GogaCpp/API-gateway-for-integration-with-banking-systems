import uuid
from fastapi import APIRouter, Depends, status

from src.schemas.document import BaseDocument, BaseDocumentList, DocumentCreatePayload, DocumentUpdatePayload
from src.services.document import DocumentService


router = APIRouter(prefix="/abc", tags=["ABC"])


@router.get("/", response_model=BaseDocumentList)
async def get_list(
    document_service: DocumentService = Depends()
):
    return await document_service.get_document_list()


@router.get("/{document_id}", response_model=BaseDocument)
async def get_document(
    document_id: uuid.UUID,
    document_service: DocumentService = Depends()
):
    return await document_service.get_document_by_id(document_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseDocument)
async def create_document(
    document: DocumentCreatePayload,
    document_service: DocumentService = Depends()
):
    return await document_service.create_document(document)


@router.patch("/{document_id}", response_model=BaseDocument)
async def update_document(
    document_id: uuid.UUID,
    document: DocumentUpdatePayload,
    document_service: DocumentService = Depends()
):
    return await document_service.update_document(document_id, document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: uuid.UUID,
    document_service: DocumentService = Depends()
):
    return await document_service.delete_document(document_id)
