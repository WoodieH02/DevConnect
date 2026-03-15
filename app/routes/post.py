from app.core.security import get_current_user
from app.database import get_session
from app.models.post import Post, PostCreate, PostResponse
from app.models.users import User
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    post = Post(**post_data.model_dump(), author_id=current_user.id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("", response_model=list[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    posts = session.exec(select(Post).offset(skip).limit(limit)).all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")
    session.delete(post)
    session.commit()
    return {"message": "Post deleted"}