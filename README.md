# SUMA - Next-Generation Learning Management System

SUMA is a modern, AI-powered Learning Management System built with FastAPI and designed to provide an intuitive and efficient learning experience for students and teachers.

## 🚀 Features

### Core Features
- **User Management**: Student, Teacher, and Admin roles with authentication
- **Course Management**: Create and manage courses with custom icons and colors
- **Task Management**: Assignments, tests, labs, projects, and quizzes
- **File Upload/Download**: Support for various file types with preview capabilities
- **Calendar Integration**: Weekly calendar view with .ics export
- **AI Assistant**: Intelligent help for students and task analysis
- **Dashboard**: Personalized dashboard with stats and upcoming tasks

### Advanced Features
- **Real-time Notifications**: Stay updated with task deadlines and announcements
- **Grade Management**: Track grades and progress across courses
- **Attendance Tracking**: Monitor student attendance
- **Resource Management**: Share course materials and resources
- **Theme Customization**: Personalize the interface
- **Mobile Responsive**: Works seamlessly on all devices

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database (easily upgradeable to PostgreSQL)
- **Alembic**: Database migration tool
- **OpenAI API**: AI assistant integration
- **JWT**: Secure authentication

### Frontend (Coming Soon)
- **Next.js**: React framework
- **TailwindCSS**: Utility-first CSS framework
- **TypeScript**: Type-safe JavaScript

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Suma
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Start the development server**
   ```bash
   python -m app.main
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

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

# OpenAI API (optional)
OPENAI_API_KEY=your-openai-api-key-here

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Default Accounts

After running `init_db.py`, you'll have these test accounts:

- **Admin**: `admin` / `admin123`
- **Teacher**: `teacher` / `teacher123`
- **Students**: `student1`, `student2` / `student123`

## 🏗️ Project Structure

```
Suma/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── crud.py              # Database operations
│   ├── utils.py             # Utility functions
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── courses.py       # Course management
│       ├── tasks.py         # Task management
│       ├── calendar.py      # Calendar and events
│       ├── ai.py            # AI assistant
│       └── files.py         # File upload/download
├── alembic/                 # Database migrations
├── uploads/                 # File upload directory
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables template
├── init_db.py              # Database initialization
└── README.md               # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
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

### Calendar
- `GET /calendar/events` - Get calendar events
- `GET /calendar/export/ics` - Export calendar as .ics
- `GET /calendar/dashboard` - Get dashboard data

### AI Assistant
- `POST /ai/query` - Query AI assistant
- `GET /ai/dashboard-summary` - Get AI dashboard summary
- `POST /ai/task-analysis` - Analyze task files

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/docs)
2. Review the [Issues](https://github.com/your-repo/issues) page
3. Create a new issue with detailed information

## 🔮 Roadmap

### Phase 1 (Current)
- ✅ Backend API with core features
- ✅ Database models and authentication
- ✅ File upload/download system
- ✅ AI assistant integration

### Phase 2 (Next)
- 🔄 Frontend with Next.js
- 🔄 Real-time notifications
- 🔄 Advanced calendar features
- 🔄 Mobile app

### Phase 3 (Future)
- 📋 Video conferencing integration
- 📋 Advanced analytics
- 📋 Multi-language support
- 📋 Plugin system

---

**SUMA LMS** - Empowering Education Through Technology 🎓
