from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models.comment import Comment, CommentCreate, CommentResponse
from app.models.post import Post
from app.models.users import User
from app.database import get_session
from app.core.security import get_current_user

router = APIRouter(prefix="/posts", tags=["comments"])

@router.post("/{post_id}/comments", response_model=CommentResponse)
def add_comment(
    post_id: int,
    comment_data: CommentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = Comment(
        content=comment_data.content,
        user_id=current_user.id,
        post_id=post_id
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

@router.get("/{post_id}/comments", response_model=list[CommentResponse])
def get_comments(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = session.exec(
        select(Comment).where(Comment.post_id == post_id)
    ).all()
    return comments

@router.delete("/{post_id}/comments/{comment_id}")
def delete_comment(
    post_id: int,
    comment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 🔒 protected
):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your comment")

    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted"}