from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional


class Contract(BaseModel):
    id: uuid.UUID
    name: str
    discription: str
    path: str


class ContractCreatePayload(BaseModel):
    name: str
    discription: str
    user_id: uuid.UUID


class ContractUpdatePayload(BaseModel):
    name: Optional[str]
    discription: Optional[str]


class BaseContract(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    id: uuid.UUID
    name: str
    discription: str
    created_at: datetime
    user_id: uuid.UUID


class BaseContractList(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    contract_list: list[BaseContract | None]


class ConnectContractDocumentPayload(BaseModel):
    contract_id: uuid.UUID
    document_id: uuid.UUID
