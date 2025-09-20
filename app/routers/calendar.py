from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user
from app.schemas import CalendarEvent, CalendarEventCreate, DashboardData, DashboardStats
from app.crud import (
    get_user_calendar_events, create_calendar_event, get_dashboard_stats,
    get_upcoming_tasks
)
from app.models import User
from ics import Calendar, Event as ICSEvent

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/events", response_model=List[CalendarEvent])
async def read_calendar_events(
    start_date: datetime = Query(..., description="Start date for events"),
    end_date: datetime = Query(..., description="End date for events"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get calendar events for current user within date range"""
    return get_user_calendar_events(db, current_user.id, start_date, end_date)


@router.post("/events", response_model=CalendarEvent)
async def create_new_event(
    event: CalendarEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new calendar event"""
    return create_calendar_event(db=db, event=event, user_id=current_user.id)


@router.get("/export/ics")
async def export_calendar_ics(
    start_date: datetime = Query(..., description="Start date for export"),
    end_date: datetime = Query(..., description="End date for export"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Export calendar events as .ics file"""
    events = get_user_calendar_events(db, current_user.id, start_date, end_date)
    
    # Create ICS calendar
    calendar = Calendar()
    
    for event in events:
        ics_event = ICSEvent()
        ics_event.name = event.title
        ics_event.description = event.description or ""
        ics_event.begin = event.start_time
        ics_event.end = event.end_time
        ics_event.all_day = event.is_all_day
        
        # Add course information if available
        if event.course:
            ics_event.description += f"\n\nCourse: {event.course.name} ({event.course.code})"
        
        calendar.events.add(ics_event)
    
    # Generate ICS content
    ics_content = str(calendar)
    
    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": f"attachment; filename=suma_calendar_{current_user.username}.ics"
        }
    )


@router.get("/dashboard", response_model=DashboardData)
async def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard data including stats and upcoming tasks"""
    # Get dashboard stats
    stats = get_dashboard_stats(db, current_user.id)
    
    # Get upcoming tasks
    upcoming_tasks = get_upcoming_tasks(db, current_user.id, 7)
    
    # Convert to UpcomingTask format
    from app.schemas import UpcomingTask
    from app.crud import get_task_submission
    
    upcoming_task_list = []
    for task in upcoming_tasks:
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
        upcoming_task_list.append(upcoming_task)
    
    # Get recent activities (placeholder for now)
    recent_activities = [
        "Completed Math Assignment 3",
        "Submitted Physics Lab Report",
        "Attended CS Lecture"
    ]
    
    return DashboardData(
        stats=DashboardStats(**stats),
        upcoming_tasks=upcoming_task_list,
        recent_activities=recent_activities
    )


@router.get("/weekly")
async def get_weekly_calendar(
    week_start: datetime = Query(..., description="Start of the week"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get weekly calendar view with tasks and events"""
    # Calculate week end
    week_end = week_start + timedelta(days=7)
    
    # Get events for the week
    events = get_user_calendar_events(db, current_user.id, week_start, week_end)
    
    # Get tasks due in the week
    from app.crud import get_user_tasks
    tasks = get_user_tasks(db, current_user.id, 7)
    
    # Filter tasks for this week
    week_tasks = [
        task for task in tasks 
        if week_start <= task.due_date <= week_end
    ]
    
    # Organize by day
    weekly_data = {}
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_key = day.strftime("%Y-%m-%d")
        
        # Get events for this day
        day_events = [
            event for event in events
            if event.start_time.date() == day.date()
        ]
        
        # Get tasks due this day
        day_tasks = [
            task for task in week_tasks
            if task.due_date.date() == day.date()
        ]
        
        weekly_data[day_key] = {
            "date": day.isoformat(),
            "events": day_events,
            "tasks": day_tasks
        }
    
    return {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "days": weekly_data
    }
