from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated, Self
from uuid import UUID

from app.utils import is_unique


class GroupCreate(BaseModel):
    description: str
    # Each group has 4 words.
    words: Annotated[list[str], Field(min_length=4, max_length=4)]


class PuzzleCreate(BaseModel):
    groups: Annotated[list[GroupCreate], Field(min_length=4, max_length=4)]

    @model_validator(mode="after")
    def validate_description_uniqueness(self) -> Self:
        if not is_unique([group.description for group in self.groups]):
            raise ValueError("Group descriptions must be unique.")
        return self

    @model_validator(mode="after")
    def validate_word_uniqueness(self) -> Self:
        if not is_unique([word for group in self.groups for word in group.words]):
            raise ValueError("Words must be unique across all groups.")
        return self


class PuzzleCreateResponse(BaseModel):
    id: UUID


class WordRetrieve(BaseModel):
    id: UUID
    text: str


class PuzzleRetrieve(BaseModel):
    id: UUID
    words: list[WordRetrieve]
