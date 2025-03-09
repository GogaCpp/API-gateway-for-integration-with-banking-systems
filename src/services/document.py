import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status

from src.database import get_async_session
from src.models.document_and_contract import Document
from src.schemas.document import DocumentCreatePayload, DocumentUpdatePayload


class DocumentService():
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    async def get_document_by_id(self, id: uuid.UUID):
        query = (
            select(Document)
            .where(
                Document.id == id
            )
        )
        document = (await self._session.execute(query)).scalars().first()
        return document

    async def get_document_list(self):
        query = (
            select(Document)
        )
        documents = (await self._session.execute(query)).scalars().all()
        return {"document_list": documents}

    async def create_document(self, document: DocumentCreatePayload):

        login = (await self._session.execute(select(Document).where(Document.name == document.name))).scalar()
        if login:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Document alredy exist")

        document = Document(
            name=document.name,
            discription=document.discription,
            path=document.path,
            user_id=document.user_id
        )

        self._session.add(document)
        await self._session.commit()
        await self._session.refresh(document)
        return document

    async def update_document(self, id: uuid.UUID, document_base: DocumentUpdatePayload):
        document = await self.get_document_by_id(id)
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        update_data = document_base.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(document, key, value)

        await self._session.commit()
        return document

    async def delete_document(self, id: uuid.UUID):
        document = await self.get_document_by_id(id)

        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self._session.delete(document)
        await self._session.commit()
