"""
SUMA LMS AI智能体系统
实现多智能体协作，提供负责任的教育性AI交互
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import json
import ollama
from app.config import settings


class AgentRole(Enum):
    """AI智能体角色"""
    LEARNING_MENTOR = "learning_mentor"  # 学习导师
    CONCEPT_EXPLAINER = "concept_explainer"  # 概念解释者
    PROBLEM_GUIDE = "problem_guide"  # 问题引导者
    WRITING_ASSISTANT = "writing_assistant"  # 写作助手
    CODE_REVIEWER = "code_reviewer"  # 代码审查者
    LEARNING_ANALYST = "learning_analyst"  # 学习分析员


@dataclass
class AgentCapabilities:
    """智能体能力定义"""
    can_explain_concepts: bool = False
    can_guide_thinking: bool = False
    can_help_writing: bool = False
    can_review_code: bool = False
    can_analyze_learning: bool = False
    can_provide_answers: bool = False  # 是否可以直接提供答案


@dataclass
class AgentLimitations:
    """智能体限制定义"""
    cannot_provide_direct_answers: bool = True
    cannot_write_complete_assignments: bool = True
    cannot_do_homework: bool = True
    must_guide_learning: bool = True


@dataclass
class UserContext:
    """用户上下文信息"""
    user_id: int
    course_id: Optional[int] = None
    task_id: Optional[int] = None
    learning_level: str = "beginner"  # beginner, intermediate, advanced
    subject_area: Optional[str] = None
    recent_topics: List[str] = None
    learning_goals: List[str] = None


class AIAgent:
    """AI智能体基类"""
    
    def __init__(self, role: AgentRole, capabilities: AgentCapabilities, 
                 limitations: AgentLimitations, system_prompt: str):
        self.role = role
        self.capabilities = capabilities
        self.limitations = limitations
        self.system_prompt = system_prompt
        self.client = ollama.Client(host=settings.ollama_base_url)
    
    async def process_query(self, query: str, context: UserContext, 
                          additional_context: str = "") -> Dict[str, Any]:
        """处理用户查询"""
        # 检查查询是否合规
        if not self._is_query_appropriate(query, context):
            return self._generate_guidance_response(query, context)
        
        # 生成响应
        response = await self._generate_response(query, context, additional_context)
        
        # 后处理响应
        processed_response = self._post_process_response(response, context)
        
        return {
            "agent_role": self.role.value,
            "response": processed_response,
            "suggestions": self._generate_suggestions(query, processed_response),
            "learning_tips": self._generate_learning_tips(context),
            "timestamp": datetime.now().isoformat()
        }
    
    def _is_query_appropriate(self, query: str, context: UserContext) -> bool:
        """检查查询是否适合当前智能体处理"""
        # 检查是否请求直接答案
        direct_answer_indicators = [
            "直接告诉我答案", "帮我写作业", "给我答案", "帮我做", 
            "直接写", "完整答案", "标准答案"
        ]
        
        for indicator in direct_answer_indicators:
            if indicator in query.lower():
                return False
        
        return True
    
    def _generate_guidance_response(self, query: str, context: UserContext) -> Dict[str, Any]:
        """Generate guidance response instead of direct answers"""
        guidance_prompts = {
            AgentRole.LEARNING_MENTOR: "I understand you want to learn, but let me first understand your learning goals and current level of understanding.",
            AgentRole.CONCEPT_EXPLAINER: "I can help you understand concepts, but let's start from the basics. Can you tell me what you currently understand about this concept?",
            AgentRole.PROBLEM_GUIDE: "I can guide your thinking through questions, but won't give direct answers. Let's first analyze the key points of the problem.",
            AgentRole.WRITING_ASSISTANT: "I can help improve your writing structure and expression, but can't write content directly. Let's discuss your ideas and structure first.",
            AgentRole.CODE_REVIEWER: "I can help review and improve your code, but can't write it directly. Let's look at your coding approach first.",
            AgentRole.LEARNING_ANALYST: "I can analyze your learning situation, but need to understand your learning goals and progress first."
        }
        
        return {
            "agent_role": self.role.value,
            "response": guidance_prompts.get(self.role, "Let me help you learn in the right way."),
            "suggestions": self._get_guidance_suggestions(),
            "learning_tips": self._generate_learning_tips(context),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_response(self, query: str, context: UserContext, 
                               additional_context: str) -> str:
        """生成AI响应"""
        full_prompt = self._build_prompt(query, context, additional_context)
        
        try:
            response = self.client.chat(
                model=settings.ollama_model,
                messages=[
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": query}
                ],
                options={
                    "temperature": 0.7,
                    "num_predict": 500
                }
            )
            return response['message']['content']
        except Exception as e:
            return f"抱歉，我暂时无法处理你的请求。请稍后再试。错误信息: {str(e)}"
    
    def _build_prompt(self, query: str, context: UserContext, 
                     additional_context: str) -> str:
        """构建完整的提示"""
        prompt_parts = [
            self.system_prompt,
            f"\n用户上下文信息:",
            f"- 学习水平: {context.learning_level}",
            f"- 课程ID: {context.course_id or '未指定'}",
            f"- 任务ID: {context.task_id or '未指定'}",
            f"- 学科领域: {context.subject_area or '未指定'}",
            f"- 最近学习主题: {', '.join(context.recent_topics or [])}",
            f"- 学习目标: {', '.join(context.learning_goals or [])}",
        ]
        
        if additional_context:
            prompt_parts.append(f"\n额外上下文: {additional_context}")
        
        prompt_parts.extend([
            "\n重要提醒:",
            "1. 不要直接提供作业答案或完整解决方案",
            "2. 通过提问和引导来帮助学生思考",
            "3. 提供学习方法和思路，而不是结果",
            "4. 鼓励学生独立思考和探索",
            "5. 如果学生要求直接答案，引导他们思考过程"
        ])
        
        return "\n".join(prompt_parts)
    
    def _post_process_response(self, response: str, context: UserContext) -> str:
        """后处理响应，确保符合教育原则"""
        # 检查响应是否包含直接答案
        if self._contains_direct_answer(response):
            return self._convert_to_guidance(response)
        
        return response
    
    def _contains_direct_answer(self, response: str) -> bool:
        """检查响应是否包含直接答案"""
        direct_answer_patterns = [
            "答案是", "结果是", "正确答案是", "标准答案是",
            "直接写", "完整代码", "完整答案", "直接告诉你"
        ]
        
        for pattern in direct_answer_patterns:
            if pattern in response:
                return True
        return False
    
    def _convert_to_guidance(self, response: str) -> str:
        """将直接答案转换为指导性内容"""
        return f"我理解你想知道答案，但让我们换个角度思考：{response}\n\n你能告诉我你的思考过程吗？这样我可以更好地帮助你学习。"
    
    def _generate_suggestions(self, query: str, response: str) -> List[str]:
        """Generate learning suggestions"""
        suggestions = [
            "Try thinking about the key points of the problem yourself",
            "List the related knowledge you already have",
            "Think about different solution methods",
            "Discuss your ideas with classmates",
            "Consult relevant learning materials"
        ]
        return suggestions[:3]  # Return first 3 suggestions
    
    def _generate_learning_tips(self, context: UserContext) -> List[str]:
        """Generate personalized learning tips"""
        tips = [
            "Regularly review learned content",
            "Actively ask questions and think",
            "Exchange learning experiences with classmates",
            "Create a study plan",
            "Keep learning notes"
        ]
        return tips[:2]  # Return first 2 tips
    
    def _get_guidance_suggestions(self) -> List[str]:
        """Get guidance suggestions"""
        return [
            "Tell me your thought process",
            "Share the methods you've already tried",
            "Describe the specific difficulties you're facing",
            "Explain your learning goals"
        ]


class LearningMentor(AIAgent):
    """学习导师智能体"""
    
    def __init__(self):
        system_prompt = """
You are an experienced learning mentor who specializes in helping students develop learning strategies and study habits.
Your goal is to guide students toward independent learning, not to provide direct answers.

Your responsibilities:
1. Help students create learning plans
2. Provide learning methods and techniques
3. Develop good study habits
4. Encourage independent thinking
5. Analyze learning progress and effectiveness

Important principles:
- Guide student thinking through questions
- Provide learning frameworks rather than specific answers
- Encourage students to explore actively
- Help students establish learning goals
- Develop critical thinking skills
        """
        
        capabilities = AgentCapabilities(
            can_explain_concepts=True,
            can_guide_thinking=True,
            can_analyze_learning=True
        )
        
        limitations = AgentLimitations(
            cannot_provide_direct_answers=True,
            cannot_write_complete_assignments=True,
            cannot_do_homework=True,
            must_guide_learning=True
        )
        
        super().__init__(AgentRole.LEARNING_MENTOR, capabilities, limitations, system_prompt)


class ConceptExplainer(AIAgent):
    """Concept Explainer Agent"""
    
    def __init__(self):
        system_prompt = """
You are a professional concept explainer who excels at explaining complex concepts in simple, understandable ways.
Your goal is to help students understand the essence of concepts, not to memorize answers.

Your responsibilities:
1. Explain complex concepts and theories
2. Provide conceptual understanding frameworks
3. Illustrate abstract concepts with examples
4. Help students build knowledge connections
5. Clarify conceptual misconceptions

Important principles:
- Start explanations from basic concepts
- Use real-life examples
- Encourage student questions
- Help students build knowledge systems
- Do not provide direct homework answers
        """
        
        capabilities = AgentCapabilities(
            can_explain_concepts=True,
            can_guide_thinking=True
        )
        
        limitations = AgentLimitations(
            cannot_provide_direct_answers=True,
            cannot_write_complete_assignments=True,
            cannot_do_homework=True,
            must_guide_learning=True
        )
        
        super().__init__(AgentRole.CONCEPT_EXPLAINER, capabilities, limitations, system_prompt)


class ProblemGuide(AIAgent):
    """Problem Guide Agent"""
    
    def __init__(self):
        system_prompt = """
You are a problem-solving guide who excels at helping students think through problems through questions and guidance.
Your goal is to develop students' critical thinking and problem-solving abilities.

Your responsibilities:
1. Guide student thinking through questions
2. Help students break down complex problems
3. Provide thinking frameworks and methods
4. Encourage students to try different approaches
5. Develop students' logical thinking

Important principles:
- Guide through questions rather than direct answers
- Help students discover key points of problems
- Encourage students to try and make mistakes
- Help students build confidence in problem-solving
- Do not provide standard answers
        """
        
        capabilities = AgentCapabilities(
            can_guide_thinking=True
        )
        
        limitations = AgentLimitations(
            cannot_provide_direct_answers=True,
            cannot_write_complete_assignments=True,
            cannot_do_homework=True,
            must_guide_learning=True
        )
        
        super().__init__(AgentRole.PROBLEM_GUIDE, capabilities, limitations, system_prompt)


class WritingAssistant(AIAgent):
    """Writing Assistant Agent"""
    
    def __init__(self):
        system_prompt = """
You are a professional writing assistant who specializes in helping students improve their writing skills and expression.
Your goal is to enhance students' writing abilities, not to write content for them.

Your responsibilities:
1. Provide writing techniques and guidance
2. Help improve article structure
3. Suggest better ways of expression
4. Provide writing frameworks and templates
5. Encourage students to express their own ideas

Important principles:
- Do not write article content directly
- Provide writing techniques and structural advice
- Encourage students to express original ideas
- Help improve expression rather than replace thinking
- Develop students' writing abilities
        """
        
        capabilities = AgentCapabilities(
            can_help_writing=True,
            can_guide_thinking=True
        )
        
        limitations = AgentLimitations(
            cannot_provide_direct_answers=True,
            cannot_write_complete_assignments=True,
            cannot_do_homework=True,
            must_guide_learning=True
        )
        
        super().__init__(AgentRole.WRITING_ASSISTANT, capabilities, limitations, system_prompt)


class CodeReviewer(AIAgent):
    """Code Reviewer Agent"""
    
    def __init__(self):
        system_prompt = """
You are a professional code reviewer who specializes in helping students improve code quality and programming skills.
Your goal is to enhance students' programming abilities, not to write code directly.

Your responsibilities:
1. Review code quality and standards
2. Provide code improvement suggestions
3. Explain programming concepts and best practices
4. Help students understand code logic
5. Develop good programming habits

Important principles:
- Do not write complete code directly
- Provide code improvement suggestions and approaches
- Explain programming concepts and principles
- Encourage independent thinking and programming
- Develop problem-solving programming mindset
        """
        
        capabilities = AgentCapabilities(
            can_review_code=True,
            can_explain_concepts=True,
            can_guide_thinking=True
        )
        
        limitations = AgentLimitations(
            cannot_provide_direct_answers=True,
            cannot_write_complete_assignments=True,
            cannot_do_homework=True,
            must_guide_learning=True
        )
        
        super().__init__(AgentRole.CODE_REVIEWER, capabilities, limitations, system_prompt)


class LearningAnalyst(AIAgent):
    """Learning Analyst Agent"""
    
    def __init__(self):
        system_prompt = """
You are a learning analysis expert who specializes in analyzing learning data and providing personalized learning recommendations.
Your goal is to help students optimize their learning process and effectiveness.

Your responsibilities:
1. Analyze learning progress and effectiveness
2. Identify weak areas in learning
3. Provide personalized learning recommendations
4. Predict learning needs and challenges
5. Optimize learning strategies and methods

Important principles:
- Provide objective analysis based on data
- Provide personalized learning recommendations
- Help students set reasonable learning goals
- Encourage continuous learning and improvement
- Do not provide direct answers to learning content
        """
        
        capabilities = AgentCapabilities(
            can_analyze_learning=True,
            can_guide_thinking=True
        )
        
        limitations = AgentLimitations(
            cannot_provide_direct_answers=True,
            cannot_write_complete_assignments=True,
            cannot_do_homework=True,
            must_guide_learning=True
        )
        
        super().__init__(AgentRole.LEARNING_ANALYST, capabilities, limitations, system_prompt)


class AgentManager:
    """智能体管理器"""
    
    def __init__(self):
        self.agents = {
            AgentRole.LEARNING_MENTOR: LearningMentor(),
            AgentRole.CONCEPT_EXPLAINER: ConceptExplainer(),
            AgentRole.PROBLEM_GUIDE: ProblemGuide(),
            AgentRole.WRITING_ASSISTANT: WritingAssistant(),
            AgentRole.CODE_REVIEWER: CodeReviewer(),
            AgentRole.LEARNING_ANALYST: LearningAnalyst()
        }
    
    async def route_query(self, query: str, context: UserContext, 
                         preferred_agent: Optional[AgentRole] = None) -> Dict[str, Any]:
        """路由查询到合适的智能体"""
        if preferred_agent and preferred_agent in self.agents:
            agent = self.agents[preferred_agent]
        else:
            agent = self._select_best_agent(query, context)
        
        return await agent.process_query(query, context)
    
    def _select_best_agent(self, query: str, context: UserContext) -> AIAgent:
        """根据查询内容选择最合适的智能体"""
        query_lower = query.lower()
        
        # 学习计划和方法相关
        if any(keyword in query_lower for keyword in ["学习计划", "学习方法", "学习策略", "学习习惯"]):
            return self.agents[AgentRole.LEARNING_MENTOR]
        
        # 概念解释相关
        elif any(keyword in query_lower for keyword in ["解释", "概念", "理论", "理解", "什么是"]):
            return self.agents[AgentRole.CONCEPT_EXPLAINER]
        
        # 问题解决相关
        elif any(keyword in query_lower for keyword in ["怎么做", "如何解决", "问题", "思路"]):
            return self.agents[AgentRole.PROBLEM_GUIDE]
        
        # 写作相关
        elif any(keyword in query_lower for keyword in ["写作", "文章", "论文", "表达", "结构"]):
            return self.agents[AgentRole.WRITING_ASSISTANT]
        
        # 编程相关
        elif any(keyword in query_lower for keyword in ["代码", "编程", "程序", "算法", "debug"]):
            return self.agents[AgentRole.CODE_REVIEWER]
        
        # 学习分析相关
        elif any(keyword in query_lower for keyword in ["分析", "进度", "效果", "建议", "评估"]):
            return self.agents[AgentRole.LEARNING_ANALYST]
        
        # 默认使用学习导师
        else:
            return self.agents[AgentRole.LEARNING_MENTOR]
    
    def get_agent_info(self, role: AgentRole) -> Dict[str, Any]:
        """获取智能体信息"""
        agent = self.agents.get(role)
        if not agent:
            return {}
        
        return {
            "role": agent.role.value,
            "capabilities": agent.capabilities.__dict__,
            "limitations": agent.limitations.__dict__,
            "description": self._get_agent_description(role)
        }
    
    def _get_agent_description(self, role: AgentRole) -> str:
        """Get agent description"""
        descriptions = {
            AgentRole.LEARNING_MENTOR: "Learning mentor, helps you create study plans and develop learning habits",
            AgentRole.CONCEPT_EXPLAINER: "Concept explainer, helps you understand complex concepts and theories",
            AgentRole.PROBLEM_GUIDE: "Problem guide, guides your thinking through questions",
            AgentRole.WRITING_ASSISTANT: "Writing assistant, helps you improve writing skills and expression",
            AgentRole.CODE_REVIEWER: "Code reviewer, helps you improve code quality and programming skills",
            AgentRole.LEARNING_ANALYST: "Learning analyst, analyzes your learning progress and provides recommendations"
        }
        return descriptions.get(role, "AI Learning Assistant")
