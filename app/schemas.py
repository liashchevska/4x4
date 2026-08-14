from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated, Self
from uuid import UUID

from app.utils import is_unique


class GroupBase(BaseModel):
    title: str
    words: Annotated[list[str], Field(min_length=4, max_length=4)]


class GroupCreate(GroupBase):
    pass


class PuzzleCreate(BaseModel):
    groups: Annotated[list[GroupCreate], Field(min_length=4, max_length=4)]

    @model_validator(mode="after")
    def validate_title_uniqueness(self) -> Self:
        if not is_unique([group.title for group in self.groups]):
            raise ValueError("Group titles must be unique.")
        return self

    @model_validator(mode="after")
    def validate_word_uniqueness(self) -> Self:
        if not is_unique([word for group in self.groups for word in group.words]):
            raise ValueError("Words must be unique across all groups.")
        return self


class PuzzleCreateResponse(BaseModel):
    id: UUID


class WordRead(BaseModel):
    id: int
    text: str


class PuzzleRead(BaseModel):
    id: UUID
    words: list[WordRead]
