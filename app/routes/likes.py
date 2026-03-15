from app.core.security import get_current_user
from app.database import get_session
from app.models.like import Like
from app.models.post import Post
from app.models.users import User
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

router = APIRouter(prefix="/posts", tags=["likes"])

@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    # Check post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if already liked
    existing_like = session.exec(
        select(Like).where(
            Like.user_id == current_user.id,
            Like.post_id == post_id
        )
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked this post")

    like = Like(user_id=current_user.id, post_id=post_id)
    session.add(like)
    session.commit()
    return {"message": "Post liked"}

@router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    like = session.exec(
        select(Like).where(
            Like.user_id == current_user.id,
            Like.post_id == post_id
        )
    ).first()

    if not like:
        raise HTTPException(status_code=404, detail="You haven't liked this post")

    session.delete(like)
    session.commit()
    return {"message": "Post unliked"}