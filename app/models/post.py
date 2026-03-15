from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.comment import Comment

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    tech_stack: str
    repo_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int = Field(foreign_key="user.id")

    author: Optional["User"] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship()

class PostCreate(SQLModel):
    title: str
    description: str
    tech_stack: str
    repo_url: Optional[str] = None

class PostResponse(SQLModel):
    id: int
    title: str
    description: str
    tech_stack: str
    repo_url: Optional[str]
    created_at: datetime
    author_id: int
    like_count: int = 0    