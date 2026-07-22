from .database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(default="default text")
