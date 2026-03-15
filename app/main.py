from app.database import create_db
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.models.users import User
from app.routes import users, auth, post, likes, comments
from fastapi import FastAPI

app = FastAPI(title="DevConnect API")

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(likes.router)
app.include_router(comments.router)
@app.get("/")
def root():
    return {"message": "Welcome to DevConnect API"}