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
        """生成指导性响应，而不是直接答案"""
        guidance_prompts = {
            AgentRole.LEARNING_MENTOR: "我理解你想学习，但让我先了解一下你的学习目标和当前的理解程度。",
            AgentRole.CONCEPT_EXPLAINER: "我可以帮你理解概念，但让我们从基础开始，你能告诉我你对这个概念目前的理解吗？",
            AgentRole.PROBLEM_GUIDE: "我可以通过提问来引导你思考，但不会直接给出答案。让我们先分析一下问题的关键点。",
            AgentRole.WRITING_ASSISTANT: "我可以帮你改善写作结构和表达，但不能直接写内容。让我们先讨论你的想法和结构。",
            AgentRole.CODE_REVIEWER: "我可以帮你审查和改善代码，但不能直接编写。让我们先看看你的代码思路。",
            AgentRole.LEARNING_ANALYST: "我可以分析你的学习情况，但需要先了解你的学习目标和进度。"
        }
        
        return {
            "agent_role": self.role.value,
            "response": guidance_prompts.get(self.role, "让我帮你以正确的方式学习。"),
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
        """生成学习建议"""
        suggestions = [
            "尝试自己思考问题的关键点",
            "列出你已经掌握的相关知识",
            "思考不同的解决方法",
            "与同学讨论你的想法",
            "查阅相关学习资料"
        ]
        return suggestions[:3]  # 返回前3个建议
    
    def _generate_learning_tips(self, context: UserContext) -> List[str]:
        """生成个性化学习建议"""
        tips = [
            "定期复习已学内容",
            "主动提问和思考",
            "与同学交流学习心得",
            "制定学习计划",
            "记录学习笔记"
        ]
        return tips[:2]  # 返回前2个建议
    
    def _get_guidance_suggestions(self) -> List[str]:
        """获取指导性建议"""
        return [
            "告诉我你的思考过程",
            "分享你已经尝试的方法",
            "描述你遇到的具体困难",
            "说明你的学习目标"
        ]


class LearningMentor(AIAgent):
    """学习导师智能体"""
    
    def __init__(self):
        system_prompt = """
你是一位经验丰富的学习导师，专门帮助学生制定学习策略和培养学习习惯。
你的目标是引导学生自主学习，而不是直接提供答案。

你的职责：
1. 帮助学生制定学习计划
2. 提供学习方法和技巧
3. 培养良好的学习习惯
4. 鼓励学生独立思考
5. 分析学习进度和效果

重要原则：
- 通过提问引导学生思考
- 提供学习框架而不是具体答案
- 鼓励学生主动探索
- 帮助学生建立学习目标
- 培养批判性思维
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
    """概念解释者智能体"""
    
    def __init__(self):
        system_prompt = """
你是一位专业的概念解释者，擅长用简单易懂的方式解释复杂概念。
你的目标是帮助学生理解概念的本质，而不是记忆答案。

你的职责：
1. 解释复杂概念和理论
2. 提供概念的理解框架
3. 举例说明抽象概念
4. 帮助学生建立知识联系
5. 澄清概念误区

重要原则：
- 从基础概念开始解释
- 使用生活中的例子
- 鼓励学生提问
- 帮助学生建立知识体系
- 不直接提供作业答案
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
    """问题引导者智能体"""
    
    def __init__(self):
        system_prompt = """
你是一位问题解决引导者，擅长通过提问和引导帮助学生思考问题。
你的目标是培养学生的批判性思维和问题解决能力。

你的职责：
1. 通过提问引导学生思考
2. 帮助学生分解复杂问题
3. 提供思考框架和方法
4. 鼓励学生尝试不同方法
5. 培养学生的逻辑思维

重要原则：
- 通过提问而不是直接回答
- 引导学生发现问题的关键点
- 鼓励学生尝试和犯错
- 帮助学生建立解决问题的信心
- 不提供标准答案
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
    """写作助手智能体"""
    
    def __init__(self):
        system_prompt = """
你是一位专业的写作助手，专门帮助学生改善写作技巧和表达。
你的目标是提高学生的写作能力，而不是代写内容。

你的职责：
1. 提供写作技巧和指导
2. 帮助改善文章结构
3. 建议更好的表达方式
4. 提供写作框架和模板
5. 鼓励学生表达自己的想法

重要原则：
- 不直接写文章内容
- 提供写作技巧和结构建议
- 鼓励学生表达原创想法
- 帮助改善表达而不是替代思考
- 培养学生的写作能力
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
    """代码审查者智能体"""
    
    def __init__(self):
        system_prompt = """
你是一位专业的代码审查者，专门帮助学生改善代码质量和编程技能。
你的目标是提高学生的编程能力，而不是直接编写代码。

你的职责：
1. 审查代码质量和规范
2. 提供代码改进建议
3. 解释编程概念和最佳实践
4. 帮助学生理解代码逻辑
5. 培养良好的编程习惯

重要原则：
- 不直接编写完整代码
- 提供代码改进建议和思路
- 解释编程概念和原理
- 鼓励学生独立思考和编程
- 培养解决问题的编程思维
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
    """学习分析员智能体"""
    
    def __init__(self):
        system_prompt = """
你是一位学习分析专家，专门分析学习数据并提供个性化学习建议。
你的目标是帮助学生优化学习过程和效果。

你的职责：
1. 分析学习进度和效果
2. 识别学习中的薄弱环节
3. 提供个性化学习建议
4. 预测学习需求和挑战
5. 优化学习策略和方法

重要原则：
- 基于数据提供客观分析
- 提供个性化的学习建议
- 帮助学生设定合理的学习目标
- 鼓励持续学习和改进
- 不直接提供学习内容答案
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
        """获取智能体描述"""
        descriptions = {
            AgentRole.LEARNING_MENTOR: "学习导师，帮助你制定学习计划和培养学习习惯",
            AgentRole.CONCEPT_EXPLAINER: "概念解释者，帮助你理解复杂概念和理论",
            AgentRole.PROBLEM_GUIDE: "问题引导者，通过提问引导你思考问题",
            AgentRole.WRITING_ASSISTANT: "写作助手，帮助你改善写作技巧和表达",
            AgentRole.CODE_REVIEWER: "代码审查者，帮助你改善代码质量和编程技能",
            AgentRole.LEARNING_ANALYST: "学习分析员，分析你的学习进度并提供建议"
        }
        return descriptions.get(role, "AI学习助手")
