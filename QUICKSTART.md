# SUMA LMS - Quick Start Guide

Get SUMA LMS up and running in minutes!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Start Server
```bash
python run.py
```

### 4. Access API
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔑 Test Accounts

After initialization, use these accounts:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Teacher | `teacher` | `teacher123` |
| Student | `student1` | `student123` |
| Student | `student2` | `student123` |

## 🧪 Test the API

Run the test script to verify everything works:
```bash
python test_api.py
```

## 📱 API Usage Examples

### Login
```bash
curl -X POST "http://localhost:8000/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "student123"}'
```

### Get User Info
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Courses
```bash
curl -X GET "http://localhost:8000/courses/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🎯 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Set up OpenAI**: Add your API key to `.env` for AI features
3. **Customize**: Modify course icons, colors, and settings
4. **Build Frontend**: Use the API to build your frontend application

## 🆘 Troubleshooting

### Server won't start?
- Check if port 8000 is available
- Ensure all dependencies are installed
- Check Python version (3.8+ required)

### Database errors?
- Delete `suma.db` and run `python init_db.py` again
- Check file permissions in the project directory

### API errors?
- Check the server logs
- Verify your authentication token
- Ensure the server is running on port 8000

---

**Happy Learning with SUMA! 🎓**
