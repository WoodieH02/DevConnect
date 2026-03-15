from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models.follow import Follow
from app.models.users import User, UserResponse
from app.database import get_session
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["follows"])

@router.post("/{username}/follow")
def follow_user(
    username: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    # Find the user to follow
    user_to_follow = session.exec(select(User).where(User.username == username)).first()
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")

    # Can't follow yourself
    if user_to_follow.id == current_user.id:
        raise HTTPException(status_code=400, detail="You can't follow yourself")

    # Check if already following
    existing = session.exec(
        select(Follow).where(
            Follow.follower_id == current_user.id,
            Follow.following_id == user_to_follow.id
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already following this user")

    follow = Follow(follower_id=current_user.id, following_id=user_to_follow.id)
    session.add(follow)
    session.commit()
    return {"message": f"You are now following {username}"}

@router.delete("/{username}/follow")
def unfollow_user(
    username: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    user_to_unfollow = session.exec(select(User).where(User.username == username)).first()
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found")

    follow = session.exec(
        select(Follow).where(
            Follow.follower_id == current_user.id,
            Follow.following_id == user_to_unfollow.id
        )
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="You are not following this user")

    session.delete(follow)
    session.commit()
    return {"message": f"You unfollowed {username}"}

@router.get("/{username}/followers", response_model=list[UserResponse])
def get_followers(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers = session.exec(
        select(User).join(Follow, Follow.follower_id == User.id)
        .where(Follow.following_id == user.id)
    ).all()
    return followers

@router.get("/{username}/following", response_model=list[UserResponse])
def get_following(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    following = session.exec(
        select(User).join(Follow, Follow.following_id == User.id)
        .where(Follow.follower_id == user.id)
    ).all()
    return following