from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user, require_teacher_or_admin
from app.schemas import Course, CourseCreate, CourseUpdate, CourseWithProgress, User
from app.crud import (
    get_courses, get_course, get_user_courses, get_teacher_courses,
    create_course, update_course, enroll_user_in_course
)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/", response_model=List[Course])
async def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all active courses"""
    if current_user.role.value == "teacher":
        return get_teacher_courses(db, current_user.id)
    else:
        return get_user_courses(db, current_user.id)


@router.get("/all", response_model=List[Course])
async def read_all_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all courses (public endpoint)"""
    return get_courses(db, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=Course)
async def read_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific course"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=Course)
async def create_new_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """Create a new course (teacher/admin only)"""
    return create_course(db=db, course=course, teacher_id=current_user.id)


@router.put("/{course_id}", response_model=Course)
async def update_course_info(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """Update course information (teacher/admin only)"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if user is the teacher of this course or admin
    if course.teacher_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this course"
        )
    
    return update_course(db=db, course_id=course_id, course_update=course_update)


@router.post("/{course_id}/enroll")
async def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Enroll in a course"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    success = enroll_user_in_course(db, current_user.id, course_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Already enrolled in this course"
        )
    
    return {"message": "Successfully enrolled in course"}


@router.get("/{course_id}/progress", response_model=CourseWithProgress)
async def get_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get course progress for current user"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Get enrollment count
    from app.models import Enrollment
    enrollment_count = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
    
    # Get task count
    from app.models import Task
    task_count = db.query(Task).filter(
        Task.course_id == course_id,
        Task.is_published == True
    ).count()
    
    # Get completed tasks count
    from app.models import TaskSubmission
    completed_tasks = db.query(TaskSubmission).join(Task).filter(
        Task.course_id == course_id,
        TaskSubmission.user_id == current_user.id,
        TaskSubmission.status == "graded"
    ).count()
    
    course_dict = course.__dict__.copy()
    course_dict.update({
        "enrollment_count": enrollment_count,
        "task_count": task_count,
        "completed_tasks": completed_tasks
    })
    
    return CourseWithProgress(**course_dict)
