import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user, require_teacher_or_admin
from app.schemas import FileUploadResponse, CourseResource, CourseResourceCreate
from app.models import User, TaskAttachment, SubmissionAttachment, CourseResource as CourseResourceModel
from app.config import settings
from app.crud import get_task, get_task_submission, create_course_resource
import aiofiles
from PIL import Image

router = APIRouter(prefix="/files", tags=["文件管理"])


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()


def is_allowed_file_type(filename: str) -> bool:
    """Check if file type is allowed"""
    allowed_extensions = {
        '.pdf', '.doc', '.docx', '.txt', '.rtf',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp',
        '.mp4', '.avi', '.mov', '.wmv',
        '.mp3', '.wav', '.m4a',
        '.zip', '.rar', '.7z',
        '.xlsx', '.xls', '.pptx', '.ppt',
        '.py', '.js', '.html', '.css', '.json', '.xml'
    }
    return get_file_extension(filename) in allowed_extensions


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename to avoid conflicts"""
    ext = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{ext}"


async def save_upload_file(upload_file: UploadFile, destination: str) -> dict:
    """Save uploaded file and return file info"""
    # Generate unique filename
    unique_filename = generate_unique_filename(upload_file.filename)
    file_path = os.path.join(destination, unique_filename)
    
    # Ensure directory exists
    os.makedirs(destination, exist_ok=True)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)
    
    # Get file size
    file_size = len(content)
    
    return {
        "filename": upload_file.filename,
        "unique_filename": unique_filename,
        "file_path": file_path,
        "file_size": file_size,
        "mime_type": upload_file.content_type
    }


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a file"""
    # Check file size
    if file.size and file.size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_file_size} bytes"
        )
    
    # Check file type
    if not is_allowed_file_type(file.filename):
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )
    
    # Save file
    file_info = await save_upload_file(file, settings.upload_dir)
    
    return FileUploadResponse(
        filename=file_info["filename"],
        file_path=file_info["file_path"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"]
    )


@router.get("/download/{file_path:path}")
async def download_file(
    file_path: str,
    current_user: User = Depends(get_current_active_user)
):
    """Download a file"""
    # Security check - ensure file is within upload directory
    full_path = os.path.join(settings.upload_dir, file_path)
    if not os.path.exists(full_path) or not full_path.startswith(settings.upload_dir):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=full_path,
        filename=os.path.basename(file_path),
        media_type='application/octet-stream'
    )


@router.post("/task/{task_id}/attachment")
async def upload_task_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """Upload attachment for a task (teacher/admin only)"""
    # Check if task exists and user has permission
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.course.teacher_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to upload attachments for this task"
        )
    
    # Check file size and type
    if file.size and file.size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_file_size} bytes"
        )
    
    if not is_allowed_file_type(file.filename):
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )
    
    # Save file
    file_info = await save_upload_file(file, settings.upload_dir)
    
    # Create database record
    attachment = TaskAttachment(
        task_id=task_id,
        filename=file_info["filename"],
        file_path=file_info["file_path"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"]
    )
    
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    
    return FileUploadResponse(
        filename=file_info["filename"],
        file_path=file_info["file_path"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"]
    )


@router.post("/submission/{submission_id}/attachment")
async def upload_submission_attachment(
    submission_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload attachment for a submission"""
    # Check if submission exists and belongs to user
    submission = db.query(SubmissionAttachment).filter(
        SubmissionAttachment.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Check file size and type
    if file.size and file.size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_file_size} bytes"
        )
    
    if not is_allowed_file_type(file.filename):
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )
    
    # Save file
    file_info = await save_upload_file(file, settings.upload_dir)
    
    # Create database record
    attachment = SubmissionAttachment(
        submission_id=submission_id,
        filename=file_info["filename"],
        file_path=file_info["file_path"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"]
    )
    
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    
    return FileUploadResponse(
        filename=file_info["filename"],
        file_path=file_info["file_path"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"]
    )


@router.post("/course/{course_id}/resource")
async def upload_course_resource(
    course_id: int,
    title: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(None),
    url: str = Form(None),
    resource_type: str = Form(...),
    is_public: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """Upload course resource (teacher/admin only)"""
    from app.crud import get_course
    
    # Check if course exists and user has permission
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.teacher_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to upload resources for this course"
        )
    
    file_path = None
    
    # Handle file upload if provided
    if file and file.filename:
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {settings.max_file_size} bytes"
            )
        
        if not is_allowed_file_type(file.filename):
            raise HTTPException(
                status_code=400,
                detail="File type not allowed"
            )
        
        file_info = await save_upload_file(file, settings.upload_dir)
        file_path = file_info["file_path"]
    
    # Create course resource
    resource_data = CourseResourceCreate(
        course_id=course_id,
        title=title,
        description=description,
        url=url,
        resource_type=resource_type,
        is_public=is_public
    )
    
    resource = create_course_resource(db, resource_data)
    
    # Update file path if file was uploaded
    if file_path:
        resource.file_path = file_path
        db.commit()
        db.refresh(resource)
    
    return resource


@router.get("/preview/{file_path:path}")
async def preview_file(
    file_path: str,
    current_user: User = Depends(get_current_active_user)
):
    """Preview a file (for images and text files)"""
    # Security check
    full_path = os.path.join(settings.upload_dir, file_path)
    if not os.path.exists(full_path) or not full_path.startswith(settings.upload_dir):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_ext = get_file_extension(file_path).lower()
    
    # Handle image previews
    if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        try:
            # Resize image for preview
            with Image.open(full_path) as img:
                img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                preview_path = full_path.replace(file_ext, f"_preview{file_ext}")
                img.save(preview_path)
                return FileResponse(preview_path)
        except Exception:
            # If preview generation fails, return original
            return FileResponse(full_path)
    
    # Handle text files
    elif file_ext in ['.txt', '.md', '.json', '.xml', '.py', '.js', '.html', '.css']:
        return FileResponse(full_path, media_type='text/plain')
    
    else:
        raise HTTPException(
            status_code=400,
            detail="File type not supported for preview"
        )


@router.delete("/attachment/{attachment_id}")
async def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an attachment"""
    # Try to find in task attachments
    attachment = db.query(TaskAttachment).filter(TaskAttachment.id == attachment_id).first()
    
    if attachment:
        # Check permissions
        if attachment.task.course.teacher_id != current_user.id and current_user.role.value != "admin":
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions to delete this attachment"
            )
        
        # Delete file
        if os.path.exists(attachment.file_path):
            os.remove(attachment.file_path)
        
        # Delete database record
        db.delete(attachment)
        db.commit()
        
        return {"message": "Attachment deleted successfully"}
    
    # Try to find in submission attachments
    attachment = db.query(SubmissionAttachment).filter(SubmissionAttachment.id == attachment_id).first()
    
    if attachment:
        # Check permissions (user can only delete their own submission attachments)
        if attachment.submission.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions to delete this attachment"
            )
        
        # Delete file
        if os.path.exists(attachment.file_path):
            os.remove(attachment.file_path)
        
        # Delete database record
        db.delete(attachment)
        db.commit()
        
        return {"message": "Attachment deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Attachment not found")
