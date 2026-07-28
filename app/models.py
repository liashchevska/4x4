from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, Uuid, String
from datetime import UTC, datetime


class Puzzle(Base):
    __tablename__ = "puzzles"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    groups: Mapped[list["Group"]] = relationship(back_populates="puzzle")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    puzzle_id: Mapped[UUID] = mapped_column(ForeignKey("puzzles.id"), nullable=False)
    puzzle: Mapped["Puzzle"] = relationship(back_populates="groups")
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    words: Mapped[list["Word"]] = relationship(back_populates="group")


class Word(Base):
    __tablename__ = "words"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped["Group"] = relationship(back_populates="words")
    text: Mapped[str] = mapped_column(String(255), nullable=False)
