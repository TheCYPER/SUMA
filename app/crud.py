from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime, timedelta
from app.models import (
    User, Course, Task, TaskSubmission, CourseResource, 
    Attendance, CalendarEvent, Enrollment, TaskAttachment, SubmissionAttachment
)
from app.schemas import (
    UserCreate, UserUpdate, CourseCreate, CourseUpdate, 
    TaskCreate, TaskUpdate, TaskSubmissionCreate, TaskSubmissionUpdate,
    CourseResourceCreate, AttendanceCreate, CalendarEventCreate
)
from app.auth import get_password_hash


# User CRUD
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user


# Course CRUD
def get_course(db: Session, course_id: int) -> Optional[Course]:
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
    return db.query(Course).filter(Course.is_active == True).offset(skip).limit(limit).all()


def get_user_courses(db: Session, user_id: int) -> List[Course]:
    return db.query(Course).join(Enrollment).filter(
        Enrollment.user_id == user_id,
        Course.is_active == True
    ).all()


def get_teacher_courses(db: Session, teacher_id: int) -> List[Course]:
    return db.query(Course).filter(
        Course.teacher_id == teacher_id,
        Course.is_active == True
    ).all()


def create_course(db: Session, course: CourseCreate, teacher_id: int) -> Course:
    db_course = Course(**course.dict(), teacher_id=teacher_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course_update: CourseUpdate) -> Optional[Course]:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        update_data = course_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_course, field, value)
        db.commit()
        db.refresh(db_course)
    return db_course


def enroll_user_in_course(db: Session, user_id: int, course_id: int) -> bool:
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()
    
    if existing:
        return False
    
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return True


# Task CRUD
def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def get_course_tasks(db: Session, course_id: int) -> List[Task]:
    return db.query(Task).filter(
        Task.course_id == course_id,
        Task.is_published == True
    ).order_by(Task.due_date).all()


def get_user_tasks(db: Session, user_id: int, days_ahead: int = 30) -> List[Task]:
    end_date = datetime.utcnow() + timedelta(days=days_ahead)
    return db.query(Task).join(Course).join(Enrollment).filter(
        Enrollment.user_id == user_id,
        Task.due_date <= end_date,
        Task.is_published == True
    ).order_by(Task.due_date).all()


def get_upcoming_tasks(db: Session, user_id: int, days_ahead: int = 7) -> List[Task]:
    end_date = datetime.utcnow() + timedelta(days=days_ahead)
    return db.query(Task).join(Course).join(Enrollment).filter(
        Enrollment.user_id == user_id,
        Task.due_date <= end_date,
        Task.due_date >= datetime.utcnow(),
        Task.is_published == True
    ).order_by(Task.due_date).all()


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
    return db_task


# Task Submission CRUD
def get_task_submission(db: Session, task_id: int, user_id: int) -> Optional[TaskSubmission]:
    return db.query(TaskSubmission).filter(
        TaskSubmission.task_id == task_id,
        TaskSubmission.user_id == user_id
    ).first()


def get_user_submissions(db: Session, user_id: int) -> List[TaskSubmission]:
    return db.query(TaskSubmission).filter(TaskSubmission.user_id == user_id).all()


def create_task_submission(db: Session, submission: TaskSubmissionCreate, user_id: int) -> TaskSubmission:
    db_submission = TaskSubmission(**submission.dict(), user_id=user_id)
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def update_task_submission(db: Session, submission_id: int, submission_update: TaskSubmissionUpdate) -> Optional[TaskSubmission]:
    db_submission = db.query(TaskSubmission).filter(TaskSubmission.id == submission_id).first()
    if db_submission:
        update_data = submission_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_submission, field, value)
        
        # Update submitted_at if status changes to submitted
        if submission_update.status == "submitted" and not db_submission.submitted_at:
            db_submission.submitted_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_submission)
    return db_submission


# Course Resource CRUD
def get_course_resources(db: Session, course_id: int) -> List[CourseResource]:
    return db.query(CourseResource).filter(CourseResource.course_id == course_id).all()


def create_course_resource(db: Session, resource: CourseResourceCreate) -> CourseResource:
    db_resource = CourseResource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


# Attendance CRUD
def get_course_attendance(db: Session, course_id: int, user_id: int) -> List[Attendance]:
    return db.query(Attendance).filter(
        Attendance.course_id == course_id,
        Attendance.user_id == user_id
    ).order_by(Attendance.date.desc()).all()


def create_attendance_record(db: Session, attendance: AttendanceCreate) -> Attendance:
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


# Calendar Event CRUD
def get_user_calendar_events(db: Session, user_id: int, start_date: datetime, end_date: datetime) -> List[CalendarEvent]:
    return db.query(CalendarEvent).filter(
        or_(
            CalendarEvent.user_id == user_id,
            CalendarEvent.course_id.in_(
                db.query(Enrollment.course_id).filter(Enrollment.user_id == user_id)
            )
        ),
        CalendarEvent.start_time >= start_date,
        CalendarEvent.end_time <= end_date
    ).order_by(CalendarEvent.start_time).all()


def create_calendar_event(db: Session, event: CalendarEventCreate, user_id: int) -> CalendarEvent:
    db_event = CalendarEvent(**event.dict(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


# Dashboard Stats
def get_dashboard_stats(db: Session, user_id: int) -> dict:
    # Get user's enrolled courses
    user_courses = get_user_courses(db, user_id)
    course_ids = [course.id for course in user_courses]
    
    # Count active tasks
    active_tasks = db.query(Task).filter(
        Task.course_id.in_(course_ids),
        Task.is_published == True,
        Task.due_date >= datetime.utcnow()
    ).count()
    
    # Count upcoming deadlines (next 7 days)
    upcoming_deadlines = db.query(Task).filter(
        Task.course_id.in_(course_ids),
        Task.is_published == True,
        Task.due_date >= datetime.utcnow(),
        Task.due_date <= datetime.utcnow() + timedelta(days=7)
    ).count()
    
    # Calculate attendance rate
    total_attendance = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.status.in_(["present", "late"])
    ).count()
    
    total_records = db.query(Attendance).filter(Attendance.user_id == user_id).count()
    attendance_rate = (total_attendance / total_records * 100) if total_records > 0 else 0
    
    return {
        "total_courses": len(user_courses),
        "active_tasks": active_tasks,
        "upcoming_deadlines": upcoming_deadlines,
        "attendance_rate": round(attendance_rate, 1)
    }
