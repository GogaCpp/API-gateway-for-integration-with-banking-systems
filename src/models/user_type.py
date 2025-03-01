import uuid
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


from src.database import Base


class UserType(Base):
    __tablename__ = 'user_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(nullable=False)
