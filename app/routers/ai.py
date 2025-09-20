from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user
from app.schemas import AIQuery, AIResponse
from app.crud import get_upcoming_tasks, get_user_courses, get_dashboard_stats
from app.models import User
from app.config import settings
import ollama
import requests
import json

router = APIRouter(prefix="/ai", tags=["AI助手"])

# Test Ollama connection
def test_ollama_connection() -> bool:
    """测试Ollama是否正在运行且可访问"""
    try:
        response = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


async def get_ai_response(query: str, context: str = "", user_id: int = None, db: Session = None) -> AIResponse:
    """使用Ollama获取用户查询的AI响应"""
    
    # Check if Ollama is running
    if not test_ollama_connection():
        return AIResponse(
            response="AI Assistant is not available. Please make sure Ollama is running on your system.\n\nTo start Ollama:\n1. Install Ollama from https://ollama.ai\n2. Run: ollama serve\n3. Pull a model: ollama pull llama3.2",
            suggestions=["Install Ollama", "Start Ollama service", "Pull a model"]
        )
    
    try:
        # Prepare context based on query type
        system_prompt = """You are SUMA, an AI assistant for a Learning Management System (LMS). 
        You help students with their academic tasks, course information, and study planning.
        Be helpful, concise, and encouraging in your responses. Respond in Chinese when appropriate."""
        
        # Add relevant context based on the query
        if "task" in query.lower() or "assignment" in query.lower() or "deadline" in query.lower():
            if db and user_id:
                upcoming_tasks = get_upcoming_tasks(db, user_id, 14)
                if upcoming_tasks:
                    task_context = "\n".join([
                        f"- {task.title} (Due: {task.due_date.strftime('%Y-%m-%d')}) - {task.course.name}"
                        for task in upcoming_tasks[:5]
                    ])
                    context += f"\n\nUpcoming tasks:\n{task_context}"
        
        if "course" in query.lower() or "class" in query.lower():
            if db and user_id:
                courses = get_user_courses(db, user_id)
                if courses:
                    course_context = "\n".join([
                        f"- {course.name} ({course.code})"
                        for course in courses
                    ])
                    context += f"\n\nEnrolled courses:\n{course_context}"
        
        # Prepare the full prompt for Ollama
        full_prompt = f"{system_prompt}\n\nContext: {context}\n\nUser Query: {query}"
        
        # Call Ollama API
        client = ollama.Client(host=settings.ollama_base_url)
        response = client.chat(
            model=settings.ollama_model,
            messages=[
                {
                    'role': 'user',
                    'content': full_prompt
                }
            ],
            options={
                'temperature': 0.7,
                'num_predict': 500
            }
        )
        
        ai_response = response['message']['content']
        
        # Generate suggestions based on the query
        suggestions = generate_suggestions(query, ai_response)
        
        return AIResponse(
            response=ai_response,
            suggestions=suggestions
        )
        
    except Exception as e:
        return AIResponse(
            response=f"抱歉，我遇到了一个错误: {str(e)}\n\n请确保:\n1. Ollama服务正在运行\n2. 模型 {settings.ollama_model} 已下载\n3. 网络连接正常",
            suggestions=["检查Ollama服务", "下载模型", "重试请求"]
        )


def generate_suggestions(query: str, response: str) -> List[str]:
    """根据查询和响应生成有用的建议"""
    suggestions = []
    
    query_lower = query.lower()
    
    if "task" in query_lower or "assignment" in query_lower or "作业" in query or "任务" in query:
        suggestions.extend([
            "查看所有即将到期的任务",
            "检查任务详情",
            "提交作业"
        ])
    
    if "course" in query_lower or "class" in query_lower or "课程" in query or "班级" in query:
        suggestions.extend([
            "查看课程材料",
            "检查课程安排",
            "联系老师"
        ])
    
    if "calendar" in query_lower or "schedule" in query_lower or "日历" in query or "日程" in query:
        suggestions.extend([
            "导出日历",
            "查看周计划",
            "添加新事件"
        ])
    
    if "grade" in query_lower or "score" in query_lower or "成绩" in query or "分数" in query:
        suggestions.extend([
            "查看成绩单",
            "检查作业反馈",
            "跟踪学习进度"
        ])
    
    # Default suggestions
    if not suggestions:
        suggestions.extend([
            "询问即将到期的任务",
            "获取课程信息",
            "查看日历事件"
        ])
    
    return suggestions[:3]  # Limit to 3 suggestions


@router.post("/query", response_model=AIResponse)
async def query_ai_assistant(
    query_data: AIQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """查询AI助手"""
    return await get_ai_response(
        query=query_data.query,
        context=query_data.context or "",
        user_id=current_user.id,
        db=db
    )


@router.get("/dashboard-summary", response_model=AIResponse)
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取AI生成的仪表板摘要"""
    # Get user's data
    stats = get_dashboard_stats(db, current_user.id)
    upcoming_tasks = get_upcoming_tasks(db, current_user.id, 7)
    courses = get_user_courses(db, current_user.id)
    
    # Create context
    context = f"""
    User: {current_user.full_name}
    Total courses: {stats['total_courses']}
    Active tasks: {stats['active_tasks']}
    Upcoming deadlines: {stats['upcoming_deadlines']}
    Attendance rate: {stats['attendance_rate']}%
    
    Upcoming tasks:
    {chr(10).join([f"- {task.title} (Due: {task.due_date.strftime('%Y-%m-%d')})" for task in upcoming_tasks[:3]])}
    
    Enrolled courses:
    {chr(10).join([f"- {course.name}" for course in courses])}
    """
    
    query = "请提供一个简洁、鼓励性的学术进度总结，并告诉我今天应该重点关注什么。"
    
    return await get_ai_response(query, context, current_user.id, db)


@router.post("/task-analysis", response_model=AIResponse)
async def analyze_task_file(
    task_id: int,
    query_data: AIQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """分析任务文件并提供AI洞察"""
    from app.crud import get_task, get_task_submission
    
    # Get task information
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get user's submission
    submission = get_task_submission(db, task_id, current_user.id)
    
    # Create context
    context = f"""
    Task: {task.title}
    Description: {task.description or 'No description provided'}
    Due Date: {task.due_date}
    Max Points: {task.max_points}
    Task Type: {task.task_type}
    Course: {task.course.name}
    
    User's Submission Status: {submission.status if submission else 'Not submitted'}
    """
    
    if submission and submission.content:
        context += f"\nSubmission Content: {submission.content}"
    
    # Add file attachments info if available
    if task.attachments:
        context += f"\nAttached Files: {', '.join([att.filename for att in task.attachments])}"
    
    return await get_ai_response(
        query=query_data.query,
        context=context,
        user_id=current_user.id,
        db=db
    )


@router.get("/study-tips", response_model=AIResponse)
async def get_study_tips(
    course_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取个性化学习建议"""
    context = ""
    
    if course_id:
        from app.crud import get_course, get_course_tasks
        course = get_course(db, course_id)
        if course:
            tasks = get_course_tasks(db, course_id)
            context = f"""
            Course: {course.name} ({course.code})
            Description: {course.description or 'No description'}
            Total Tasks: {len(tasks)}
            """
    else:
        # General study tips
        courses = get_user_courses(db, current_user.id)
        context = f"""
        Student: {current_user.full_name}
        Enrolled in {len(courses)} courses
        """
    
    query = "请根据我当前的学术情况提供个性化的学习建议和策略。"
    
    return await get_ai_response(query, context, current_user.id, db)


@router.get("/status")
async def get_ai_status():
    """检查AI助手状态和可用模型"""
    is_connected = test_ollama_connection()
    
    if not is_connected:
        return {
            "status": "disconnected",
            "message": "Ollama服务未运行",
            "suggestion": "请启动Ollama服务: ollama serve"
        }
    
    try:
        # Get available models
        client = ollama.Client(host=settings.ollama_base_url)
        models = client.list()
        
        available_models = [model.model for model in models.models]
        current_model = settings.ollama_model
        
        return {
            "status": "connected",
            "message": "AI助手已就绪",
            "current_model": current_model,
            "available_models": available_models,
            "ollama_url": settings.ollama_base_url
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"连接Ollama时出错: {str(e)}",
            "suggestion": "请检查Ollama服务状态"
        }
