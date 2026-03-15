from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.post import Post

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")

class CommentCreate(SQLModel):
    content: str

class CommentResponse(SQLModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    post_id: int