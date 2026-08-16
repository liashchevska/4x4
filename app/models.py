from __future__ import annotations
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, Uuid, String
from datetime import UTC, datetime
from enum import Enum

WORDS_PER_GROUP = 4


class GuessResult(Enum):
    INCORRECT = 0
    CORRECT = WORDS_PER_GROUP
    ONEAWAY = WORDS_PER_GROUP - 1

    @classmethod
    def _missing_(cls, value):
        return cls.INCORRECT


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
    def create(cls, session: Session, *, group_list: list) -> "Puzzle":
        """Create a new Puzzle instance along with its associated Groups and Words."""
        _words = lambda words: [Word(text=word) for word in words]
        groups = [
            Group(
                title=group["title"],
                words=_words(group["words"]),
            )
            for group in group_list
        ]

        puzzle = cls(groups=groups)
        session.add(puzzle)
        session.flush()

        return puzzle

    def guess(self, guess: list[int]) -> tuple[GuessResult, Group | None]:
        for group in self.groups:
            group_result = group.guess(guess)

            if group_result != GuessResult.INCORRECT:
                return group_result, group if group_result == GuessResult.CORRECT else None

        return group_result, None


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    puzzle_id: Mapped[UUID] = mapped_column(ForeignKey("puzzles.id"), nullable=False)
    puzzle: Mapped["Puzzle"] = relationship(back_populates="groups")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    words: Mapped[list["Word"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )

    @property
    def word_ids(self):
        return [word.id for word in self.words]

    def guess(self, guess: list[int]) -> GuessResult:
        matched = len(set(self.word_ids) & set(guess))
        return GuessResult(matched)


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped["Group"] = relationship(back_populates="words")
    text: Mapped[str] = mapped_column(String(255), nullable=False)
