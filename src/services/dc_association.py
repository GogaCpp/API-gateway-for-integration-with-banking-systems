from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.database import get_async_session
from src.models.document_and_contract import DocumentContractAssociation
from src.schemas.contract import ConnectContractDocumentPayload


class DC_ConnectService():
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    async def get_connection_by_ids(self, data: ConnectContractDocumentPayload):
        query = (
            select(DocumentContractAssociation)
            .where(
                DocumentContractAssociation.document_id == data.document_id,
                DocumentContractAssociation.contract_id == data.contract_id
            )
        )
        result = (await self._session.execute(query)).scalars().first()
        return result 

    async def connect_to_document(self, data: ConnectContractDocumentPayload):

        new_association = DocumentContractAssociation(
            document_id=data.document_id,
            contract_id=data.contract_id
        )

        await self._session.merge(new_association)
        await self._session.commit()

    async def get_connection_list(self):
        return (await self._session.execute((select(DocumentContractAssociation)))).scalars().all()

    async def delete_association(self, data: ConnectContractDocumentPayload):

        con = self.get_connection_by_ids(data)
        if con is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await self._session.delete(con)
        await self._session.commit()
