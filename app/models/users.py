from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import Post

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    bio: Optional[str] = None
    github_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    posts: List["Post"] = Relationship(back_populates="author")

class UserRegister(SQLModel):
    username: str
    email: str
    password: str

class UserResponse(SQLModel):
    id: int
    username: str
    email: str
    bio: Optional[str]
    github_url: Optional[str]
    created_at: datetime