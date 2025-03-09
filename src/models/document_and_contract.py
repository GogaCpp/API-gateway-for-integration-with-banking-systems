import uuid
from sqlalchemy import TIMESTAMP, UUID, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.database import Base


class DocumentContractAssociation(Base):
    __tablename__ = "document_contract_association"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), primary_key=True
    )
    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"), primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )

    document: Mapped["Document"] = relationship(back_populates="contract_associations")
    contract: Mapped["Contract"] = relationship(back_populates="document_associations")


class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str]
    discription: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), default=uuid.uuid4
    )

    contract_associations: Mapped[list["DocumentContractAssociation"]] = relationship(
        back_populates="document",
    )

    @property
    def contracts(self):
        return [association.contract for association in self.contract_associations]


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    discription: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), default=uuid.uuid4
    )

    document_associations: Mapped[list["DocumentContractAssociation"]] = relationship(
        back_populates="contract",
    )

    @property
    def documents(self):
        return [association.document for association in self.document_associations]
