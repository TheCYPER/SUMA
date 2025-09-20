# SUMA - Next-Generation Learning Management System

SUMA is a modern, AI-powered Learning Management System built with FastAPI and Ollama, designed to provide an intuitive and efficient learning experience for students and teachers.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Ollama](https://img.shields.io/badge/Ollama-AI%20Powered-purple.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 🎯 Core Features
- **👥 User Management**: Student, Teacher, and Admin roles with JWT authentication
- **📚 Course Management**: Create and manage courses with custom icons and colors
- **📝 Task Management**: Assignments, tests, labs, projects, and quizzes
- **📁 File Upload/Download**: Support for various file types with preview capabilities
- **📅 Calendar Integration**: Weekly calendar view with .ics export
- **🤖 AI Assistant**: Multi-agent AI system with responsible educational guidance
- **📊 Dashboard**: Personalized dashboard with stats and upcoming tasks

### 🚀 Advanced Features
- **🔔 Real-time Notifications**: Stay updated with task deadlines and announcements
- **📈 Grade Management**: Track grades and progress across courses
- **📋 Attendance Tracking**: Monitor student attendance
- **📖 Resource Management**: Share course materials and resources
- **🎨 Theme Customization**: Personalize the interface
- **📱 Mobile Responsive**: Works seamlessly on all devices

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database (easily upgradeable to PostgreSQL)
- **Alembic**: Database migration tool
- **Ollama**: Local AI model integration
- **JWT**: Secure authentication
- **Pydantic**: Data validation and settings management

### AI Integration
- **Ollama**: Local AI model server
- **Llama 3.1**: Large language model for intelligent assistance
- **Chinese Language Support**: Native Chinese language processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai) (for AI features)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/suma-lms.git
cd suma-lms
```

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3.1:8b
```

### 4. Setup Ollama (for AI features)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull a model (in another terminal)
ollama pull llama3.1:8b
```

### 5. Initialize Database
```bash
python init_db.py
```

### 6. Start the Server
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=sqlite:///./suma.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Default Test Accounts

After running `init_db.py`, you'll have these test accounts:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Teacher | `teacher` | `teacher123` |
| Student | `student1` | `student123` |
| Student | `student2` | `student123` |

## 🧪 Testing

### Run API Tests
```bash
# Test all functionality
python test_ai_system.py

# Test specific API endpoints
python test_api.py
```

### Test AI Features
```bash
# Check AI status
curl http://localhost:8000/ai/status

# Test AI query (after login)
curl -X POST "http://localhost:8000/ai/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "你好，请介绍一下我的学习进度"}'
```

## 🏗️ Project Structure

```
Suma/
├── app/                    # Main application code
│   ├── routers/           # API route handlers
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── courses.py     # Course management
│   │   ├── tasks.py       # Task management
│   │   ├── calendar.py    # Calendar and events
│   │   ├── ai.py          # AI assistant (Ollama)
│   │   └── files.py       # File upload/download
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic data schemas
│   ├── crud.py           # Database operations
│   ├── auth.py           # Authentication logic
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── utils.py          # Utility functions
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── uploads/              # File upload directory
├── requirements.txt      # Python dependencies
├── env.example          # Environment variables template
├── init_db.py           # Database initialization
├── test_*.py            # Test scripts
├── AI_USAGE_GUIDE.md    # AI usage guide
├── QUICKSTART.md        # Quick start guide
└── README.md            # This file
```

## 🔌 Key API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login-json` - User login
- `GET /auth/me` - Get current user info

### Courses
- `GET /courses/` - Get user's courses
- `POST /courses/` - Create new course (teacher/admin)
- `GET /courses/{id}` - Get course details
- `POST /courses/{id}/enroll` - Enroll in course

### Tasks
- `GET /tasks/` - Get user's tasks
- `GET /tasks/upcoming` - Get upcoming tasks
- `POST /tasks/` - Create task (teacher/admin)
- `GET /tasks/{id}` - Get task details
- `POST /tasks/{id}/submission` - Submit task

### AI Assistant
- `GET /ai/status` - Check AI assistant status
- `POST /ai/query` - Query AI assistant
- `GET /ai/dashboard-summary` - Get AI dashboard summary
- `POST /ai/task-analysis` - Analyze task files
- `GET /ai/study-tips` - Get personalized study tips

### Calendar & Dashboard
- `GET /calendar/events` - Get calendar events
- `GET /calendar/export/ics` - Export calendar as .ics
- `GET /calendar/dashboard` - Get dashboard data

### Files
- `POST /files/upload` - Upload file
- `GET /files/download/{path}` - Download file
- `GET /files/preview/{path}` - Preview file

## 🚀 Deployment

### Development
```bash
python -m app.main
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker (Coming Soon)
```bash
docker build -t suma-lms .
docker run -p 8000:8000 suma-lms
```

## 🤖 AI Features

SUMA LMS includes a powerful AI assistant powered by Ollama:

- **Local AI**: No external API keys required
- **Chinese Support**: Native Chinese language processing
- **Smart Suggestions**: Context-aware recommendations
- **Task Analysis**: Analyze uploaded files and provide insights
- **Learning Tips**: Personalized study strategies
- **Progress Tracking**: AI-powered academic progress analysis

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/docs)
2. Review the [Issues](https://github.com/your-username/suma-lms/issues) page
3. Create a new issue with detailed information
4. Check [AI_USAGE_GUIDE.md](AI_USAGE_GUIDE.md) for AI usage help

## 🔮 Roadmap

### Phase 1 ✅ (Current)
- ✅ Backend API with core features
- ✅ Database models and authentication
- ✅ File upload/download system
- ✅ Ollama AI assistant integration
- ✅ Chinese language support

### Phase 2 🔄 (Next)
- 🔄 Frontend with Next.js
- 🔄 Real-time notifications
- 🔄 Advanced calendar features
- 🔄 Mobile app

### Phase 3 📋 (Future)
- 📋 Video conferencing integration
- 📋 Advanced analytics
- 📋 Multi-language support
- 📋 Plugin system
- 📋 Advanced AI features

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [Ollama](https://ollama.ai/) - Local AI model server
- [SQLAlchemy](https://sqlalchemy.org/) - Database ORM
- [Pydantic](https://pydantic.dev/) - Data validation

---

**SUMA LMS** - Empowering Education Through Technology 🎓

*Built with ❤️ for the future of learning*
