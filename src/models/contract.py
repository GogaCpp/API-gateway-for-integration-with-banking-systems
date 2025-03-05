import uuid
from sqlalchemy import TIMESTAMP, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .document import Document
from src.database import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )

    document_list: Mapped[list['Document']] = relationship(back_populates='contracts', cascade='all, delete-orphan')