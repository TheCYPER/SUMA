# SUMA - Next-Generation Learning Management System

SUMA is a modern, AI-powered Learning Management System built with FastAPI and React, designed to provide an intuitive and efficient learning experience for students and teachers.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
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
- **SQLite/PostgreSQL**: Database support
- **Alembic**: Database migration tool
- **Ollama**: Local AI model integration
- **JWT**: Secure authentication
- **Pydantic**: Data validation and settings management

### Frontend
- **React 18**: Modern frontend framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **React Query**: Data fetching and caching

### AI Integration
- **Ollama**: Local AI model server
- **Multi-Agent System**: Specialized AI agents for different educational needs
- **Chinese/English Support**: Bilingual AI responses
- **Educational Guardrails**: Prevents academic misconduct

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- [Ollama](https://ollama.ai) (for AI features)

### Backend Setup

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/suma-lms.git
cd suma-lms
```

2. **Setup Python Environment**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3.1:8b
```

4. **Setup Ollama (for AI features)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull a model (in another terminal)
ollama pull llama3.1:8b
```

5. **Initialize Database**
```bash
python init_db.py
```

6. **Start Backend Server**
```bash
python -m app.main
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Start Development Server**
```bash
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔑 Test Accounts

After initialization, use these accounts:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Teacher | `teacher` | `teacher123` |
| Student | `student1` | `student123` |
| Student | `student2` | `student123` |

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🏗️ Project Structure

```
Suma/
├── app/                    # Backend application
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
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API services
│   │   ├── utils/         # Utility functions
│   │   └── types/         # TypeScript types
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
├── alembic/              # Database migrations
├── uploads/              # File upload directory
├── requirements.txt      # Python dependencies
├── env.example          # Environment variables template
├── init_db.py           # Database initialization
├── test_*.py            # Test scripts
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-container setup
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

## 🤖 AI Features

SUMA LMS includes a powerful AI assistant powered by Ollama:

- **Local AI**: No external API keys required
- **Multi-Agent System**: Specialized agents for different educational needs
- **Educational Guardrails**: Prevents academic misconduct
- **Chinese/English Support**: Bilingual AI responses
- **Smart Suggestions**: Context-aware recommendations
- **Task Analysis**: Analyze uploaded files and provide insights
- **Learning Tips**: Personalized study strategies
- **Progress Tracking**: AI-powered academic progress analysis

## 🧪 Testing

### Backend Tests
```bash
# Test all functionality
python test_ai_system.py

# Test specific API endpoints
python test_api.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Development
```bash
# Backend
python -m app.main

# Frontend
cd frontend && npm run dev
```

### Production with Docker
```bash
# Build and start all services
docker-compose up -d

# Initialize database
docker-compose exec suma-lms python init_db.py
```

### Cloud Deployment
- **Railway**: Connect GitHub repository and deploy
- **Render**: Web service with automatic builds
- **Heroku**: Traditional PaaS deployment
- **Vercel**: Frontend deployment with serverless functions

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

## 🔮 Roadmap

### Phase 1 ✅ (Current)
- ✅ Backend API with core features
- ✅ Database models and authentication
- ✅ File upload/download system
- ✅ Ollama AI assistant integration
- ✅ React frontend with TypeScript

### Phase 2 🔄 (Next)
- 🔄 Real-time notifications with WebSocket
- 🔄 Advanced calendar features
- 🔄 Mobile app with React Native
- 🔄 Advanced AI capabilities

### Phase 3 📋 (Future)
- 📋 Video conferencing integration
- 📋 Advanced analytics dashboard
- 📋 Multi-language support
- 📋 Plugin system
- 📋 Advanced AI features

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [React](https://reactjs.org/) - The frontend framework
- [Ollama](https://ollama.ai/) - Local AI model server
- [SQLAlchemy](https://sqlalchemy.org/) - Database ORM
- [Pydantic](https://pydantic.dev/) - Data validation

---

**SUMA LMS** - Empowering Education Through Technology 🎓

*Built with ❤️ for the future of learning*