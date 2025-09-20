from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, TaskType, TaskStatus, AttendanceStatus


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    theme_preference: Optional[str] = None


class User(UserBase):
    id: int
    avatar_url: Optional[str] = None
    theme_preference: str = "light"
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Course Schemas
class CourseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: str = "#3B82F6"


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None


class Course(CourseBase):
    id: int
    teacher_id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    teacher: User
    
    class Config:
        from_attributes = True


class CourseWithProgress(Course):
    enrollment_count: int = 0
    task_count: int = 0
    completed_tasks: int = 0


# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: TaskType
    due_date: datetime
    max_points: float = 100.0


class TaskCreate(TaskBase):
    course_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    task_type: Optional[TaskType] = None
    due_date: Optional[datetime] = None
    max_points: Optional[float] = None
    is_published: Optional[bool] = None


class TaskAttachment(BaseModel):
    id: int
    filename: str
    file_size: int
    mime_type: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class Task(TaskBase):
    id: int
    course_id: int
    is_published: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    course: Course
    attachments: List[TaskAttachment] = []
    
    class Config:
        from_attributes = True


class TaskWithSubmission(Task):
    submission: Optional['TaskSubmission'] = None


# Task Submission Schemas
class TaskSubmissionBase(BaseModel):
    content: Optional[str] = None


class TaskSubmissionCreate(TaskSubmissionBase):
    task_id: int


class TaskSubmissionUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[TaskStatus] = None


class SubmissionAttachment(BaseModel):
    id: int
    filename: str
    file_size: int
    mime_type: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class TaskSubmission(TaskSubmissionBase):
    id: int
    task_id: int
    user_id: int
    status: TaskStatus = TaskStatus.NOT_STARTED
    points_earned: Optional[float] = None
    feedback: Optional[str] = None
    submitted_at: Optional[datetime] = None
    graded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: User
    attachments: List[SubmissionAttachment] = []
    
    class Config:
        from_attributes = True


# Course Resource Schemas
class CourseResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    resource_type: str
    is_public: bool = True


class CourseResourceCreate(CourseResourceBase):
    course_id: int


class CourseResource(CourseResourceBase):
    id: int
    course_id: int
    file_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Attendance Schemas
class AttendanceBase(BaseModel):
    date: datetime
    status: AttendanceStatus
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    user_id: int
    course_id: int


class Attendance(AttendanceBase):
    id: int
    user_id: int
    course_id: int
    recorded_at: datetime
    user: User
    
    class Config:
        from_attributes = True


# Calendar Event Schemas
class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    event_type: str
    is_all_day: bool = False
    color: str = "#3B82F6"


class CalendarEventCreate(CalendarEventBase):
    course_id: Optional[int] = None


class CalendarEvent(CalendarEventBase):
    id: int
    course_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    course: Optional[Course] = None
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_courses: int
    active_tasks: int
    upcoming_deadlines: int
    attendance_rate: float


class UpcomingTask(BaseModel):
    id: int
    title: str
    course_name: str
    course_icon: Optional[str] = None
    course_color: str = "#3B82F6"
    due_date: datetime
    task_type: TaskType
    status: TaskStatus
    days_until_due: int


class DashboardData(BaseModel):
    stats: DashboardStats
    upcoming_tasks: List[UpcomingTask]
    recent_activities: List[str] = []


# AI Assistant Schemas
class AIQuery(BaseModel):
    query: str
    context: Optional[str] = None


class AIResponse(BaseModel):
    response: str
    suggestions: List[str] = []


# File Upload Schemas
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    mime_type: str


# Update forward references
TaskWithSubmission.model_rebuild()
