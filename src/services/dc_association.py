from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from src.database import get_async_session
from src.models.document_and_contract import DocumentContractAssociation
from src.schemas.contract import ConnectContractDocumentPayload


class DC_ConnectService():
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    async def connect_to_document(self, data: ConnectContractDocumentPayload):

        new_association = DocumentContractAssociation(
            document_id=data.document_id,
            contract_id=data.contract_id
        )

        await self._session.merge(new_association)
        await self._session.commit()

    async def get_connection_list(self):
        return (await self._session.execute((select(DocumentContractAssociation)))).scalars().all()