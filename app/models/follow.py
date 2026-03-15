from sqlmodel import Field, SQLModel
from typing import Optional

class Follow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    follower_id: int = Field(foreign_key="user.id")   # the user who follows
    following_id: int = Field(foreign_key="user.id")  # the user being followed