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

router = APIRouter(prefix="/courses", tags=["课程"])


@router.get("/", response_model=List[Course])
async def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取所有活跃课程"""
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
    """获取所有课程（公开端点）"""
    return get_courses(db, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=Course)
async def read_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取特定课程"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="课程未找到")
    return course


@router.post("/", response_model=Course)
async def create_new_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """创建新课程（仅教师/管理员）"""
    return create_course(db=db, course=course, teacher_id=current_user.id)


@router.put("/{course_id}", response_model=Course)
async def update_course_info(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """更新课程信息（仅教师/管理员）"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="课程未找到")
    
    # 检查用户是否为该课程的教师或管理员
    if course.teacher_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限更新此课程"
        )
    
    return update_course(db=db, course_id=course_id, course_update=course_update)


@router.post("/{course_id}/enroll")
async def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """注册课程"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="课程未找到")
    
    success = enroll_user_in_course(db, current_user.id, course_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="已注册此课程"
        )
    
    return {"message": "成功注册课程"}


@router.get("/{course_id}/progress", response_model=CourseWithProgress)
async def get_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户的课程进度"""
    course = get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="课程未找到")
    
    # 获取注册人数
    from app.models import Enrollment
    enrollment_count = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
    
    # 获取任务数量
    from app.models import Task
    task_count = db.query(Task).filter(
        Task.course_id == course_id,
        Task.is_published == True
    ).count()
    
    # 获取已完成任务数量
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
