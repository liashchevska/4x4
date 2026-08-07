from app.database import Base
from app.schemas import PuzzleCreate
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, Uuid, String
from datetime import UTC, datetime


class Puzzle(Base):
    __tablename__ = "puzzles"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    groups: Mapped[list["Group"]] = relationship(
        back_populates="puzzle", cascade="all, delete-orphan"
    )

    @property
    def words(self) -> list["Word"]:
        return [word for group in self.groups for word in group.words]

    @classmethod
    def create(cls, session: Session, *, data: PuzzleCreate) -> "Puzzle":
        """Create a new Puzzle instance along with its associated Groups and Words."""
        _words = lambda words: [Word(text=word) for word in words]
        groups = [
            Group(
                description=group.description,
                words=_words(group.words),
            )
            for group in data.groups
        ]

        puzzle = cls(groups=groups)
        session.add(puzzle)
        session.flush()

        return puzzle


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    puzzle_id: Mapped[UUID] = mapped_column(ForeignKey("puzzles.id"), nullable=False)
    puzzle: Mapped["Puzzle"] = relationship(back_populates="groups")
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    words: Mapped[list["Word"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )


class Word(Base):
    __tablename__ = "words"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped["Group"] = relationship(back_populates="words")
    text: Mapped[str] = mapped_column(String(255), nullable=False)
