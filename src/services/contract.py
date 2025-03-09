import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status

from src.database import get_async_session
from src.models.document_and_contract import Contract
from src.schemas.contract import ContractCreatePayload, ContractUpdatePayload


class ContractService():
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    async def get_contract_by_id(self, id: uuid.UUID):
        query = (
            select(Contract)
            .where(
                Contract.id == id
            )
        )
        contract = (await self._session.execute(query)).scalars().first()

        return contract

    async def get_contract_list(self):
        query = (
            select(Contract)
        )
        contracts = (await self._session.execute(query)).scalars().all()
        contracts
        return {"contract_list": contracts}

    async def create_contract(self, contract: ContractCreatePayload):

        login = (await self._session.execute(select(Contract).where(Contract.name == contract.name))).scalar()
        if login:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Contract alredy exist")

        contract = Contract(
            name=contract.name,
            discription=contract.discription,
            user_id=contract.user_id
        )

        self._session.add(contract)
        await self._session.commit()
        await self._session.refresh(contract)
        return contract

    async def update_contract(self, id: uuid.UUID, contract_base: ContractUpdatePayload):
        contract = await self.get_contract_by_id(id)
        if not contract:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        update_data = contract_base.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(contract, key, value)

        await self._session.commit()
        return contract

    async def delete_contract(self, id: uuid.UUID):
        contract = await self.get_contract_by_id(id)

        if not contract:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self._session.delete(contract)
        await self._session.commit()

