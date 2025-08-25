# 🚀 FastAPI Todo App

A modern, secure, and scalable Todo API built with FastAPI, featuring JWT authentication, SQLAlchemy ORM, and comprehensive testing.

## ✨ Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 📝 **CRUD Operations** - Create, read, update, and delete todos
- 👤 **User Management** - User registration, login, and profile management
- 🗄️ **Database Integration** - SQLAlchemy ORM with SQLite/PostgreSQL support
- 🧪 **Comprehensive Testing** - Pytest test suite with 100% coverage
- 📚 **Auto-generated API Docs** - Interactive Swagger UI and ReDoc
- 🔒 **Security Features** - Password hashing, CORS middleware, input validation
- 🏥 **Health Checks** - Built-in health monitoring endpoints

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 (SQLite/PostgreSQL)
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt with passlib
- **Testing**: pytest with httpx
- **Documentation**: Auto-generated Swagger UI & ReDoc
- **Settings**: Pydantic Settings with environment variable support

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   .venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (optional)
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite:///./todo_app.db
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=True
   ```

## 🏃‍♂️ Running the Application

### Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=username&password=password123
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <your-jwt-token>
```

### Todo Endpoints

#### Create Todo
```http
POST /todos/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the FastAPI todo app"
}
```

#### Get All Todos
```http
GET /todos/
Authorization: Bearer <your-jwt-token>
```

#### Update Todo
```http
PUT /todos/{todo_id}
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

#### Delete Todo
```http
DELETE /todos/{todo_id}
Authorization: Bearer <your-jwt-token>
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

### Test Coverage
The project includes comprehensive tests for:
- ✅ User registration and authentication
- ✅ Todo CRUD operations
- ✅ JWT token validation
- ✅ Database operations
- ✅ Error handling

## 🏗️ Project Structure

```
todo-app/
├── alembic/                 # Database migrations
├── app/
│   ├── __init__.py
│   ├── auth.py              # Authentication utilities
│   ├── config.py            # Application settings
│   ├── database.py          # Database configuration
│   ├── dependencies.py      # FastAPI dependencies
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   └── todos.py         # Todo routes
│   └── schemas.py           # Pydantic models
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration
│   ├── test_auth.py         # Authentication tests
│   └── test_todos.py        # Todo tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

The application uses Pydantic Settings for configuration management. Key settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./todo_app.db` | Database connection string |
| `SECRET_KEY` | `your-super-secret-key-change-this-in-production` | JWT secret key |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |
| `DEBUG` | `True` | Debug mode |

## 🚀 Deployment

### Using Docker (Recommended)

1. **Build the Docker image**
   ```bash
   docker build -t todo-app .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 todo-app
   ```

### Manual Deployment

1. **Set production environment variables**
   ```env
   DATABASE_URL=postgresql://user:password@localhost/todo_db
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ```

2. **Run with a production ASGI server**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/docs)
2. Review the test files for usage examples
3. Open an issue on GitHub
4. Check the FastAPI documentation: https://fastapi.tiangolo.com/

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [pytest](https://docs.pytest.org/) - Testing framework

---

⭐ **Star this repository if you find it helpful!**
