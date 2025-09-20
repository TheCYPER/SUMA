from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import User, Course, Task, TaskSubmission
from app.schemas import UserRole, TaskType, TaskStatus


def create_sample_data(db: Session):
    """为测试和开发创建示例数据"""
    
    # Create sample users
    from app.auth import get_password_hash
    
    # Admin user
    admin_user = User(
        email="admin@suma.edu",
        username="admin",
        full_name="System Administrator",
        role=UserRole.ADMIN,
        hashed_password=get_password_hash("admin123"),
        is_active=True
    )
    
    # Teacher user
    teacher_user = User(
        email="teacher@suma.edu",
        username="teacher",
        full_name="Dr. Jane Smith",
        role=UserRole.TEACHER,
        hashed_password=get_password_hash("teacher123"),
        is_active=True
    )
    
    # Student users
    student1 = User(
        email="student1@suma.edu",
        username="student1",
        full_name="Alice Johnson",
        role=UserRole.STUDENT,
        hashed_password=get_password_hash("student123"),
        is_active=True
    )
    
    student2 = User(
        email="student2@suma.edu",
        username="student2",
        full_name="Bob Wilson",
        role=UserRole.STUDENT,
        hashed_password=get_password_hash("student123"),
        is_active=True
    )
    
    # Add users to database
    db.add_all([admin_user, teacher_user, student1, student2])
    db.commit()
    db.refresh(admin_user)
    db.refresh(teacher_user)
    db.refresh(student1)
    db.refresh(student2)
    
    # Create sample courses
    math_course = Course(
        name="Mathematics 101",
        code="MATH101",
        description="Introduction to Calculus and Algebra",
        icon="📐",
        color="#FF6B6B",
        teacher_id=teacher_user.id,
        is_active=True
    )
    
    cs_course = Course(
        name="Computer Science 101",
        code="CS101",
        description="Introduction to Programming",
        icon="💻",
        color="#4ECDC4",
        teacher_id=teacher_user.id,
        is_active=True
    )
    
    physics_course = Course(
        name="Physics 101",
        code="PHYS101",
        description="Introduction to Physics",
        icon="⚛️",
        color="#45B7D1",
        teacher_id=teacher_user.id,
        is_active=True
    )
    
    db.add_all([math_course, cs_course, physics_course])
    db.commit()
    db.refresh(math_course)
    db.refresh(cs_course)
    db.refresh(physics_course)
    
    # Enroll students in courses
    from app.models import Enrollment
    
    enrollments = [
        Enrollment(user_id=student1.id, course_id=math_course.id),
        Enrollment(user_id=student1.id, course_id=cs_course.id),
        Enrollment(user_id=student1.id, course_id=physics_course.id),
        Enrollment(user_id=student2.id, course_id=math_course.id),
        Enrollment(user_id=student2.id, course_id=cs_course.id),
    ]
    
    db.add_all(enrollments)
    db.commit()
    
    # Create sample tasks
    now = datetime.utcnow()
    
    math_task1 = Task(
        title="Calculus Assignment 1",
        description="Solve the following calculus problems and show your work.",
        task_type=TaskType.ASSIGNMENT,
        course_id=math_course.id,
        due_date=now + timedelta(days=7),
        max_points=100.0,
        is_published=True
    )
    
    cs_task1 = Task(
        title="Python Programming Lab",
        description="Write a Python program to implement a calculator.",
        task_type=TaskType.LAB,
        course_id=cs_course.id,
        due_date=now + timedelta(days=5),
        max_points=50.0,
        is_published=True
    )
    
    physics_task1 = Task(
        title="Physics Midterm Exam",
        description="Midterm examination covering chapters 1-5.",
        task_type=TaskType.TEST,
        course_id=physics_course.id,
        due_date=now + timedelta(days=10),
        max_points=100.0,
        is_published=True
    )
    
    db.add_all([math_task1, cs_task1, physics_task1])
    db.commit()
    db.refresh(math_task1)
    db.refresh(cs_task1)
    db.refresh(physics_task1)
    
    # Create sample submissions
    submission1 = TaskSubmission(
        task_id=math_task1.id,
        user_id=student1.id,
        content="I have completed the calculus assignment. Here are my solutions...",
        status=TaskStatus.SUBMITTED,
        points_earned=85.0,
        feedback="Good work! Minor errors in problem 3.",
        submitted_at=now + timedelta(days=6)
    )
    
    submission2 = TaskSubmission(
        task_id=cs_task1.id,
        user_id=student1.id,
        content="Here is my Python calculator implementation...",
        status=TaskStatus.GRADED,
        points_earned=48.0,
        feedback="Excellent implementation! Very clean code.",
        submitted_at=now + timedelta(days=4),
        graded_at=now + timedelta(days=4, hours=2)
    )
    
    db.add_all([submission1, submission2])
    db.commit()
    
    print("Sample data created successfully!")
    print(f"Admin user: admin / admin123")
    print(f"Teacher user: teacher / teacher123")
    print(f"Student users: student1, student2 / student123")


def get_course_icon(course_name: str) -> str:
    """Get appropriate icon for course based on name"""
    course_lower = course_name.lower()
    
    if any(word in course_lower for word in ['math', 'calculus', 'algebra', 'geometry']):
        return "📐"
    elif any(word in course_lower for word in ['computer', 'programming', 'software', 'cs']):
        return "💻"
    elif any(word in course_lower for word in ['physics', 'science']):
        return "⚛️"
    elif any(word in course_lower for word in ['chemistry', 'chem']):
        return "🧪"
    elif any(word in course_lower for word in ['biology', 'bio']):
        return "🧬"
    elif any(word in course_lower for word in ['english', 'literature', 'writing']):
        return "📚"
    elif any(word in course_lower for word in ['history', 'social']):
        return "🏛️"
    elif any(word in course_lower for word in ['art', 'design', 'creative']):
        return "🎨"
    elif any(word in course_lower for word in ['music', 'audio']):
        return "🎵"
    elif any(word in course_lower for word in ['business', 'economics', 'finance']):
        return "💼"
    else:
        return "📖"


def get_task_color(task_type: TaskType) -> str:
    """Get color for task based on type"""
    color_map = {
        TaskType.ASSIGNMENT: "#3B82F6",  # Blue
        TaskType.TEST: "#EF4444",        # Red
        TaskType.LAB: "#10B981",         # Green
        TaskType.PROJECT: "#8B5CF6",     # Purple
        TaskType.QUIZ: "#F59E0B",        # Orange
    }
    return color_map.get(task_type, "#6B7280")  # Gray default


def format_due_date(due_date: datetime) -> str:
    """Format due date for display"""
    now = datetime.utcnow()
    diff = due_date - now
    
    if diff.days < 0:
        return f"Overdue by {abs(diff.days)} days"
    elif diff.days == 0:
        return "Due today"
    elif diff.days == 1:
        return "Due tomorrow"
    elif diff.days < 7:
        return f"Due in {diff.days} days"
    else:
        return due_date.strftime("%B %d, %Y")


def calculate_grade_percentage(points_earned: float, max_points: float) -> float:
    """Calculate grade percentage"""
    if max_points == 0:
        return 0.0
    return round((points_earned / max_points) * 100, 1)


def get_grade_letter(percentage: float) -> str:
    """Get letter grade based on percentage"""
    if percentage >= 97:
        return "A+"
    elif percentage >= 93:
        return "A"
    elif percentage >= 90:
        return "A-"
    elif percentage >= 87:
        return "B+"
    elif percentage >= 83:
        return "B"
    elif percentage >= 80:
        return "B-"
    elif percentage >= 77:
        return "C+"
    elif percentage >= 73:
        return "C"
    elif percentage >= 70:
        return "C-"
    elif percentage >= 67:
        return "D+"
    elif percentage >= 63:
        return "D"
    elif percentage >= 60:
        return "D-"
    else:
        return "F"
