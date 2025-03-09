import uuid
from fastapi import APIRouter, Depends, status

from src.schemas.contract import (
    BaseContract, BaseContractList,
    ConnectContractDocumentPayload, ContractCreatePayload,
    ContractUpdatePayload
)
from src.services.contract import ContractService
from src.services.dc_association import DC_ConnectService


router = APIRouter(prefix="/cm", tags=["CM"])


@router.get("/", response_model=BaseContractList)
async def get_list(
    contract_service: ContractService = Depends()
):
    return await contract_service.get_contract_list()


@router.get("/{contract_id}", response_model=BaseContract)
async def get_contract(
    contract_id: uuid.UUID,
    contract_service: ContractService = Depends()
):
    return await contract_service.get_contract_by_id(contract_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseContract)
async def create_contract(
    contract: ContractCreatePayload,
    contract_service: ContractService = Depends()
):
    return await contract_service.create_contract(contract)


@router.patch("/{contract_id}", response_model=BaseContract)
async def update_contract(
    contract_id: uuid.UUID,
    contract: ContractUpdatePayload,
    contract_service: ContractService = Depends()
):
    return await contract_service.update_contract(contract_id, contract)


@router.delete("/{contract_id}")
async def delete_contract(
    contract_id: uuid.UUID,
    contract_service: ContractService = Depends()
):
    return await contract_service.delete_contract(contract_id)


@router.post("/connect_document")
async def connect_document_to_contract(
    data: ConnectContractDocumentPayload,
    connect_service: DC_ConnectService = Depends()
):
    return await connect_service.connect_to_document(data)
