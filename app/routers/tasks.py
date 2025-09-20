from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user, require_teacher_or_admin
from app.schemas import (
    Task, TaskCreate, TaskUpdate, TaskWithSubmission,
    TaskSubmission, TaskSubmissionCreate, TaskSubmissionUpdate,
    UpcomingTask
)
from app.crud import (
    get_task, get_course_tasks, get_user_tasks, get_upcoming_tasks,
    create_task, update_task, get_task_submission, create_task_submission,
    update_task_submission, get_user_submissions
)
from app.models import User

router = APIRouter(prefix="/tasks", tags=["任务"])


@router.get("/", response_model=List[Task])
async def read_user_tasks(
    days_ahead: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户的任务"""
    return get_user_tasks(db, current_user.id, days_ahead)


@router.get("/upcoming", response_model=List[UpcomingTask])
async def read_upcoming_tasks(
    days_ahead: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户即将到期的任务"""
    tasks = get_upcoming_tasks(db, current_user.id, days_ahead)
    upcoming_tasks = []
    
    from datetime import datetime
    for task in tasks:
        days_until_due = (task.due_date - datetime.utcnow()).days
        
        # Get user's submission for this task
        submission = get_task_submission(db, task.id, current_user.id)
        status = submission.status if submission else "not_started"
        
        upcoming_task = UpcomingTask(
            id=task.id,
            title=task.title,
            course_name=task.course.name,
            course_icon=task.course.icon,
            course_color=task.course.color,
            due_date=task.due_date,
            task_type=task.task_type,
            status=status,
            days_until_due=days_until_due
        )
        upcoming_tasks.append(upcoming_task)
    
    return upcoming_tasks


@router.get("/course/{course_id}", response_model=List[Task])
async def read_course_tasks(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取特定课程的任务"""
    return get_course_tasks(db, course_id)


@router.get("/{task_id}", response_model=TaskWithSubmission)
async def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取特定任务及用户提交内容"""
    task = get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    
    # 获取用户对此任务的提交
    submission = get_task_submission(db, task_id, current_user.id)
    
    task_dict = task.__dict__.copy()
    task_dict["submission"] = submission
    
    return TaskWithSubmission(**task_dict)


@router.post("/", response_model=Task)
async def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """创建新任务（仅教师/管理员）"""
    # 验证用户是否为该课程的教师
    from app.crud import get_course
    course = get_course(db, task.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="课程未找到")
    
    if course.teacher_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限为此课程创建任务"
        )
    
    return create_task(db=db, task=task)


@router.put("/{task_id}", response_model=Task)
async def update_task_info(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """Update task information (teacher/admin only)"""
    task = get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if user is the teacher of this course or admin
    if task.course.teacher_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this task"
        )
    
    return update_task(db=db, task_id=task_id, task_update=task_update)


# Task Submission endpoints
@router.get("/{task_id}/submission", response_model=TaskSubmission)
async def get_my_submission(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's submission for a task"""
    submission = get_task_submission(db, task_id, current_user.id)
    if submission is None:
        raise HTTPException(status_code=404, detail="No submission found")
    return submission


@router.post("/{task_id}/submission", response_model=TaskSubmission)
async def create_my_submission(
    task_id: int,
    submission: TaskSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create or update submission for a task"""
    # Check if task exists
    task = get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if submission already exists
    existing_submission = get_task_submission(db, task_id, current_user.id)
    if existing_submission:
        raise HTTPException(
            status_code=400,
            detail="Submission already exists. Use PUT to update."
        )
    
    submission_data = submission.dict()
    submission_data["task_id"] = task_id
    
    return create_task_submission(
        db=db,
        submission=TaskSubmissionCreate(**submission_data),
        user_id=current_user.id
    )


@router.put("/{task_id}/submission", response_model=TaskSubmission)
async def update_my_submission(
    task_id: int,
    submission_update: TaskSubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update current user's submission for a task"""
    submission = get_task_submission(db, task_id, current_user.id)
    if submission is None:
        raise HTTPException(status_code=404, detail="No submission found")
    
    return update_task_submission(
        db=db,
        submission_id=submission.id,
        submission_update=submission_update
    )


@router.get("/submissions/my", response_model=List[TaskSubmission])
async def read_my_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all submissions by current user"""
    return get_user_submissions(db, current_user.id)
