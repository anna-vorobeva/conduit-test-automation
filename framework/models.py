from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    """Rejects unknown fields, so any change in the API contract is noticed immediately."""

    model_config = ConfigDict(extra="forbid")


class User(StrictModel):
    username: str
    email: str
    bio: str | None
    image: str | None
    token: str


class Profile(StrictModel):
    username: str
    bio: str | None
    image: str | None
    following: bool


class Article(StrictModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: list[str] = Field(alias="tagList")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    favorited: bool
    favorites_count: int = Field(alias="favoritesCount")
    author: Profile


class Comment(StrictModel):
    id: int
    body: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    author: Profile
