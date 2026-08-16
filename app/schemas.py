from pydantic import BaseModel, Field, model_validator, computed_field, ConfigDict
from typing_extensions import Annotated, Self
from uuid import UUID
from app.utils import is_unique
from app.models import GuessResult

# In   -> data coming into a write endpoint
# Out  -> data returned from a write endpoint
# Read -> data returned from a read endpoint


class WordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str


class GroupBase[T](BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    words: Annotated[list[T], Field(min_length=4, max_length=4)]


class GroupIn(GroupBase[str]):
    pass


class GroupOut(GroupBase[int]):
    pass


class PuzzleIn(BaseModel):
    groups: Annotated[list[GroupIn], Field(min_length=4, max_length=4)]

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


class PuzzleOut(BaseModel):
    id: UUID


class PuzzleRead(BaseModel):
    id: UUID
    words: list[WordRead]
