"""
SUMA LMS AI路由 - 多智能体系统
提供负责任的教育性AI交互
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user
from app.schemas import AIQuery, AIResponse, User
from app.crud import get_upcoming_tasks, get_user_courses, get_dashboard_stats
from app.models import User
from app.config import settings
from app.ai_agents import AgentManager, AgentRole, UserContext
from app.ai_guardrails import guardrail_system
import ollama
import requests
import json
from datetime import datetime

router = APIRouter(prefix="/ai", tags=["AI助手"])

# 初始化智能体管理器
agent_manager = AgentManager()


def test_ollama_connection() -> bool:
    """测试Ollama是否正在运行且可访问"""
    try:
        response = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def build_user_context(user: User, course_id: Optional[int] = None, 
                      task_id: Optional[int] = None, db: Session = None) -> UserContext:
    """构建用户上下文信息"""
    # 获取用户最近的学习主题
    recent_topics = []
    if db:
        try:
            upcoming_tasks = get_upcoming_tasks(db, user.id, 30)
            recent_topics = list(set([task.course.name for task in upcoming_tasks[:5]]))
        except:
            pass
    
    # 根据用户角色确定学习水平
    learning_level = "beginner"
    if user.role.value == "teacher":
        learning_level = "advanced"
    elif user.role.value == "admin":
        learning_level = "expert"
    
    return UserContext(
        user_id=user.id,
        course_id=course_id,
        task_id=task_id,
        learning_level=learning_level,
        subject_area=None,  # 可以根据课程信息推断
        recent_topics=recent_topics,
        learning_goals=["提高学习效率", "掌握核心概念", "培养批判性思维"]
    )


@router.post("/query", response_model=AIResponse)
async def query_ai_assistant(
    query_data: AIQuery,
    agent_type: Optional[str] = Query(None, description="指定AI智能体类型"),
    course_id: Optional[int] = Query(None, description="课程ID"),
    task_id: Optional[int] = Query(None, description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """查询AI助手 - 多智能体系统"""
    
    # 检查Ollama连接
    if not test_ollama_connection():
        return AIResponse(
            response="AI Assistant is temporarily unavailable. Please ensure Ollama service is running.\n\nSetup steps:\n1. Install Ollama: https://ollama.ai\n2. Start service: ollama serve\n3. Pull model: ollama pull llama3.1:8b",
            suggestions=["Check Ollama service status", "Restart Ollama", "Check network connection"]
        )
    
    try:
        # 检查查询是否合规
        guardrail_result = guardrail_system.check_query(
            user_id=current_user.id,
            query=query_data.query,
            context={"course_id": course_id, "task_id": task_id}
        )
        
        # 如果查询被阻止，返回教育干预
        if not guardrail_result["allowed"]:
            if guardrail_result["action"] == "intervention":
                intervention = guardrail_result["intervention"]
                return AIResponse(
                    response=intervention["message"],
                    suggestions=intervention["suggestions"],
                    learning_tips=["Responsible AI use", "Independent thinking", "Academic integrity"],
                    agent_role="guardrail_system",
                    timestamp=intervention["timestamp"]
                )
            else:
                return AIResponse(
                    response=guardrail_result["message"],
                    suggestions=guardrail_result.get("suggestions", []),
                    learning_tips=["Contact administrator", "Review usage guidelines"],
                    agent_role="guardrail_system",
                    timestamp=datetime.now().isoformat()
                )
        
        # 构建用户上下文
        context = build_user_context(current_user, course_id, task_id, db)
        
        # 选择智能体
        preferred_agent = None
        if agent_type:
            try:
                preferred_agent = AgentRole(agent_type)
            except ValueError:
                pass
        
        # 路由查询到合适的智能体
        result = await agent_manager.route_query(
            query=query_data.query,
            context=context,
            preferred_agent=preferred_agent
        )
        
        return AIResponse(
            response=result["response"],
            suggestions=result["suggestions"],
            learning_tips=result.get("learning_tips", []),
            agent_role=result["agent_role"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        return AIResponse(
            response=f"Error processing your request: {str(e)}",
            suggestions=["Please rephrase your question", "Check network connection", "Try again later"]
        )


@router.get("/agents")
async def get_available_agents():
    """获取可用的AI智能体列表"""
    agents_info = {}
    for role in AgentRole:
        agents_info[role.value] = agent_manager.get_agent_info(role)
    
    return {
        "agents": agents_info,
        "total_count": len(AgentRole),
        "description": "SUMA LMS多智能体系统，提供负责任的教育性AI交互"
    }


@router.get("/agents/{agent_type}")
async def get_agent_details(agent_type: str):
    """获取特定智能体的详细信息"""
    try:
        role = AgentRole(agent_type)
        return agent_manager.get_agent_info(role)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"智能体类型 '{agent_type}' 不存在"
        )


@router.get("/dashboard-summary", response_model=AIResponse)
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取AI生成的仪表板摘要"""
    
    if not test_ollama_connection():
        return AIResponse(
            response="AI Assistant is temporarily unavailable, cannot generate dashboard summary.",
            suggestions=["Check Ollama service status", "Restart Ollama"]
        )
    
    try:
        # 获取用户数据
        context = build_user_context(current_user, db=db)
        
        # 使用学习分析员智能体
        result = await agent_manager.route_query(
            query="请分析我的学习情况并提供个性化建议",
            context=context,
            preferred_agent=AgentRole.LEARNING_ANALYST
        )
        
        return AIResponse(
            response=result["response"],
            suggestions=result["suggestions"],
            learning_tips=result.get("learning_tips", []),
            agent_role=result["agent_role"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        return AIResponse(
            response=f"Error generating dashboard summary: {str(e)}",
            suggestions=["Try again later", "Check data integrity"]
        )


@router.post("/task-analysis", response_model=AIResponse)
async def analyze_task_file(
    task_id: int,
    query_data: AIQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """分析任务文件并提供AI洞察"""
    
    if not test_ollama_connection():
        return AIResponse(
            response="AI Assistant is temporarily unavailable, cannot analyze task files.",
            suggestions=["Check Ollama service status", "Restart Ollama"]
        )
    
    try:
        # 构建用户上下文
        context = build_user_context(current_user, task_id=task_id, db=db)
        
        # 根据任务类型选择智能体
        # 这里可以根据任务类型（编程、写作、数学等）选择不同的智能体
        preferred_agent = AgentRole.PROBLEM_GUIDE  # 默认使用问题引导者
        
        result = await agent_manager.route_query(
            query=f"请帮我分析这个任务：{query_data.query}",
            context=context,
            preferred_agent=preferred_agent
        )
        
        return AIResponse(
            response=result["response"],
            suggestions=result["suggestions"],
            learning_tips=result.get("learning_tips", []),
            agent_role=result["agent_role"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        return AIResponse(
            response=f"Error analyzing task: {str(e)}",
            suggestions=["Check task ID", "Try again later"]
        )


@router.get("/study-tips", response_model=AIResponse)
async def get_study_tips(
    course_id: Optional[int] = Query(None, description="课程ID"),
    subject: Optional[str] = Query(None, description="学科领域"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取个性化学习建议"""
    
    if not test_ollama_connection():
        return AIResponse(
            response="AI Assistant is temporarily unavailable, cannot provide study tips.",
            suggestions=["Check Ollama service status", "Restart Ollama"]
        )
    
    try:
        # 构建用户上下文
        context = build_user_context(current_user, course_id=course_id, db=db)
        if subject:
            context.subject_area = subject
        
        # 使用学习导师智能体
        result = await agent_manager.route_query(
            query="请为我提供个性化的学习建议和学习方法",
            context=context,
            preferred_agent=AgentRole.LEARNING_MENTOR
        )
        
        return AIResponse(
            response=result["response"],
            suggestions=result["suggestions"],
            learning_tips=result.get("learning_tips", []),
            agent_role=result["agent_role"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        return AIResponse(
            response=f"Error getting study tips: {str(e)}",
            suggestions=["Try again later", "Check course information"]
        )


@router.get("/status")
async def get_ai_status():
    """检查AI助手状态和可用模型"""
    
    try:
        # 检查Ollama连接
        is_connected = test_ollama_connection()
        
        if not is_connected:
            return {
            "status": "error",
            "message": "Ollama service is not running",
            "suggestion": "Please start Ollama service: ollama serve",
            "agents_available": False,
            "available_models": [],
            "current_model": None
        }
        
        # 获取可用模型
        try:
            client = ollama.Client(host=settings.ollama_base_url)
            models = client.list()
            available_models = [model.model for model in models.models]
        except:
            available_models = []
        
        return {
            "status": "healthy",
            "message": "AI Assistant system is running normally",
            "agents_available": True,
            "available_agents": [role.value for role in AgentRole],
            "available_models": available_models,
            "current_model": settings.ollama_model,
            "ollama_url": settings.ollama_base_url,
            "features": [
                "Multi-agent collaboration",
                "Responsible AI interaction",
                "Education-oriented design",
                "Learning analytics",
                "Personalized recommendations"
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error checking AI status: {str(e)}",
            "suggestion": "Please check Ollama service status",
            "agents_available": False,
            "available_models": [],
            "current_model": None
        }


@router.post("/conversation")
async def start_conversation(
    query_data: AIQuery,
    conversation_type: str = Query("general", description="对话类型: general, learning, problem_solving, writing, coding"),
    course_id: Optional[int] = Query(None, description="课程ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """开始与AI的对话式交互"""
    
    if not test_ollama_connection():
        return AIResponse(
            response="AI助手暂时不可用，无法开始对话。",
            suggestions=["检查Ollama服务状态", "重新启动Ollama"]
        )
    
    try:
        # 根据对话类型选择智能体
        agent_mapping = {
            "general": AgentRole.LEARNING_MENTOR,
            "learning": AgentRole.LEARNING_MENTOR,
            "problem_solving": AgentRole.PROBLEM_GUIDE,
            "writing": AgentRole.WRITING_ASSISTANT,
            "coding": AgentRole.CODE_REVIEWER
        }
        
        preferred_agent = agent_mapping.get(conversation_type, AgentRole.LEARNING_MENTOR)
        
        # 构建用户上下文
        context = build_user_context(current_user, course_id=course_id, db=db)
        
        # 开始对话
        result = await agent_manager.route_query(
            query=query_data.query,
            context=context,
            preferred_agent=preferred_agent
        )
        
        return AIResponse(
            response=result["response"],
            suggestions=result["suggestions"],
            learning_tips=result.get("learning_tips", []),
            agent_role=result["agent_role"],
            timestamp=result["timestamp"],
            conversation_type=conversation_type
        )
        
    except Exception as e:
        return AIResponse(
            response=f"Error starting conversation: {str(e)}",
            suggestions=["Rephrase your question", "Try again later"]
        )


@router.get("/guardrails/user-report")
async def get_user_guardrail_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取用户护栏系统报告"""
    try:
        report = guardrail_system.get_user_report(current_user.id)
        return {
            "status": "success",
            "report": report,
            "message": "User guardrail report generated successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating user report: {str(e)}"
        )


@router.get("/guardrails/system-stats")
async def get_guardrail_system_stats(
    current_user: User = Depends(get_current_active_user)
):
    """获取护栏系统统计信息（仅管理员）"""
    # 检查用户权限
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    
    try:
        stats = guardrail_system.get_system_stats()
        return {
            "status": "success",
            "stats": stats,
            "message": "System statistics retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving system statistics: {str(e)}"
        )


@router.post("/guardrails/test-query")
async def test_query_guardrails(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """测试查询护栏系统（用于调试）"""
    try:
        result = guardrail_system.check_query(
            user_id=current_user.id,
            query=query,
            context={"test": True}
        )
        return {
            "status": "success",
            "result": result,
            "message": "查询护栏测试完成"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"测试护栏系统时出错: {str(e)}"
        )
