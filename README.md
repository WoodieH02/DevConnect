# DevConnect API 🧑‍💻

A community platform REST API for developers to share projects and get feedback. Built with Python + FastAPI.

🌐 **Live API**: [devconnect-xbij.onrender.com](https://devconnect-xbij.onrender.com)
📚 **Interactive Docs**: [devconnect-xbij.onrender.com/docs](https://devconnect-xbij.onrender.com/docs)

> ⚠️ Hosted on Render free tier — the app may take ~30 seconds to wake up on first request after inactivity.

---

## Features

- 🔐 User registration & JWT authentication
- 👤 Developer profiles with bio and GitHub link
- 📝 Create and manage project posts
- ❤️ Like and unlike posts
- 💬 Comment on posts
- 👥 Follow and unfollow developers
- 🛡️ Protected routes with role-based access

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLModel |
| Authentication | JWT (python-jose) |
| Password Hashing | bcrypt |
| Local DB | Docker |
| Deployment | Render |
| Testing | Pytest |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker Desktop

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/devconnect.git
cd devconnect
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate:
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL with Docker

```bash
docker run --name devconnect-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=devconnect \
  -p 5432:5432 \
  -d postgres
```

### 5. Configure environment variables

Create a `.env` file in the root directory:

```bash
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/devconnect
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run the app

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

---

## Running Tests

```bash
python -m pytest tests/ -v
```

---

## API Documentation

FastAPI auto-generates interactive documentation. Once the app is running visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Or try the live version:

- **Swagger UI**: https://devconnect-xbij.onrender.com/docs
- **ReDoc**: https://devconnect-xbij.onrender.com/redoc

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/login` | Login and get JWT token | ❌ |

### Users
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/users/register` | Register a new user | ❌ |
| GET | `/users/me` | Get current user profile | ✅ |
| GET | `/users/{username}` | Get a user by username | ❌ |
| DELETE | `/users/{username}` | Delete a user | ✅ |

### Posts
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/posts` | Create a new post | ✅ |
| GET | `/posts` | List all posts | ❌ |
| GET | `/posts/{post_id}` | Get a single post | ❌ |
| DELETE | `/posts/{post_id}` | Delete a post | ✅ |

### Likes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/posts/{post_id}/like` | Like a post | ✅ |
| DELETE | `/posts/{post_id}/like` | Unlike a post | ✅ |

### Comments
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/posts/{post_id}/comments` | Add a comment | ✅ |
| GET | `/posts/{post_id}/comments` | Get all comments on a post | ❌ |
| DELETE | `/posts/{post_id}/comments/{comment_id}` | Delete a comment | ✅ |

### Follows
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/users/{username}/follow` | Follow a user | ✅ |
| DELETE | `/users/{username}/follow` | Unfollow a user | ✅ |
| GET | `/users/{username}/followers` | Get a user's followers | ❌ |
| GET | `/users/{username}/following` | Get who a user follows | ❌ |

---

## Project Structure

```
devconnect/
├── app/
│   ├── main.py           # App entry point
│   ├── database.py       # DB connection & session
│   ├── core/
│   │   └── security.py   # JWT logic & get_current_user
│   ├── models/
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── like.py
│   │   ├── comment.py
│   │   └── follow.py
│   └── routes/
│       ├── auth.py
│       ├── users.py
│       ├── posts.py
│       ├── likes.py
│       ├── comments.py
│       └── follows.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_posts.py
├── Procfile
├── requirements.txt
└── README.md
```

---

## Roadmap

- [ ] Search by tech stack
- [ ] Notifications
- [ ] Refresh tokens
- [ ] Rate limiting
- [ ] Deploy to AWS

---

## License

MIT
