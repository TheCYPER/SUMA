"""
SUMA LMS AI护栏系统
防止学术不端行为，确保负责任使用AI
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import re
import json


class ViolationType(Enum):
    """违规类型"""
    DIRECT_ANSWER_REQUEST = "direct_answer_request"  # 直接答案请求
    HOMEWORK_DOING = "homework_doing"  # 作业代写
    PLAGIARISM_REQUEST = "plagiarism_request"  # 抄袭请求
    EXCESSIVE_USAGE = "excessive_usage"  # 过度使用
    INAPPROPRIATE_CONTENT = "inappropriate_content"  # 不当内容


@dataclass
class ViolationRecord:
    """违规记录"""
    user_id: int
    violation_type: ViolationType
    query: str
    timestamp: datetime
    severity: int  # 1-5, 5最严重
    action_taken: str
    context: Dict = None


class ContentFilter:
    """内容过滤器"""
    
    def __init__(self):
        # Direct answer request patterns
        self.direct_answer_patterns = [
            r"directly tell me the answer",
            r"give me the answer",
            r"help me with homework",
            r"do it for me",
            r"write it directly",
            r"complete answer",
            r"standard answer",
            r"tell me the result",
            r"give me the code",
            r"help me complete",
            r"write for me",
            r"do my homework",
            r"give it to me directly",
            r"complete solution",
            r"just tell me",
            r"show me the answer"
        ]
        
        # Homework doing patterns
        self.homework_patterns = [
            r"write my paper",
            r"write my report",
            r"write my code",
            r"do my experiment",
            r"write my program",
            r"complete my project",
            r"write my homework",
            r"write for me",
            r"do it for me",
            r"complete code",
            r"complete program",
            r"help me write",
            r"write my assignment"
        ]
        
        # Plagiarism request patterns
        self.plagiarism_patterns = [
            r"copy",
            r"plagiarize",
            r"copy directly",
            r"use directly",
            r"without changes",
            r"exactly the same",
            r"identical",
            r"copy from",
            r"steal from"
        ]
        
        # Inappropriate content patterns
        self.inappropriate_patterns = [
            r"cheat",
            r"deceive",
            r"fake",
            r"false",
            r"dishonest",
            r"fraud"
        ]
    
    def check_query(self, query: str) -> List[Tuple[ViolationType, int]]:
        """检查查询是否违规"""
        violations = []
        query_lower = query.lower()
        
        # 检查直接答案请求
        for pattern in self.direct_answer_patterns:
            if re.search(pattern, query_lower):
                violations.append((ViolationType.DIRECT_ANSWER_REQUEST, 3))
                break
        
        # 检查作业代写
        for pattern in self.homework_patterns:
            if re.search(pattern, query_lower):
                violations.append((ViolationType.HOMEWORK_DOING, 4))
                break
        
        # 检查抄袭请求
        for pattern in self.plagiarism_patterns:
            if re.search(pattern, query_lower):
                violations.append((ViolationType.PLAGIARISM_REQUEST, 5))
                break
        
        # 检查不当内容
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, query_lower):
                violations.append((ViolationType.INAPPROPRIATE_CONTENT, 5))
                break
        
        return violations


class UsageMonitor:
    """使用监控器"""
    
    def __init__(self):
        self.user_usage = {}  # {user_id: [query_timestamps]}
        self.violation_records = []  # 违规记录
    
    def record_query(self, user_id: int, query: str, timestamp: datetime = None):
        """记录用户查询"""
        if timestamp is None:
            timestamp = datetime.now()
        
        if user_id not in self.user_usage:
            self.user_usage[user_id] = []
        
        self.user_usage[user_id].append({
            "query": query,
            "timestamp": timestamp
        })
        
        # 只保留最近7天的记录
        cutoff_time = datetime.now() - timedelta(days=7)
        self.user_usage[user_id] = [
            record for record in self.user_usage[user_id]
            if record["timestamp"] > cutoff_time
        ]
    
    def check_usage_frequency(self, user_id: int) -> bool:
        """检查使用频率是否过高"""
        if user_id not in self.user_usage:
            return False
        
        now = datetime.now()
        recent_queries = [
            record for record in self.user_usage[user_id]
            if (now - record["timestamp"]).total_seconds() < 3600  # 最近1小时
        ]
        
        # 如果1小时内超过20次查询，认为使用过度
        return len(recent_queries) > 20
    
    def get_user_stats(self, user_id: int) -> Dict:
        """获取用户使用统计"""
        if user_id not in self.user_usage:
            return {
                "total_queries": 0,
                "recent_queries": 0,
                "average_daily": 0
            }
        
        now = datetime.now()
        total_queries = len(self.user_usage[user_id])
        recent_queries = len([
            record for record in self.user_usage[user_id]
            if (now - record["timestamp"]).total_seconds() < 86400  # 最近24小时
        ])
        
        # 计算平均每日查询数
        if self.user_usage[user_id]:
            first_query = min(record["timestamp"] for record in self.user_usage[user_id])
            days = (now - first_query).days + 1
            average_daily = total_queries / days
        else:
            average_daily = 0
        
        return {
            "total_queries": total_queries,
            "recent_queries": recent_queries,
            "average_daily": round(average_daily, 2)
        }
    
    def record_violation(self, violation: ViolationRecord):
        """记录违规行为"""
        self.violation_records.append(violation)
        
        # 只保留最近30天的违规记录
        cutoff_time = datetime.now() - timedelta(days=30)
        self.violation_records = [
            record for record in self.violation_records
            if record.timestamp > cutoff_time
        ]
    
    def get_user_violations(self, user_id: int) -> List[ViolationRecord]:
        """获取用户违规记录"""
        return [
            record for record in self.violation_records
            if record.user_id == user_id
        ]
    
    def should_restrict_user(self, user_id: int) -> bool:
        """判断是否应该限制用户"""
        violations = self.get_user_violations(user_id)
        
        # 如果最近7天有严重违规（严重程度4-5），则限制
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_severe_violations = [
            v for v in violations
            if v.timestamp > recent_cutoff and v.severity >= 4
        ]
        
        return len(recent_severe_violations) >= 3


class EducationalIntervention:
    """教育干预系统"""
    
    def __init__(self):
        self.intervention_messages = {
            ViolationType.DIRECT_ANSWER_REQUEST: {
                "message": "I understand you want to get answers quickly, but giving you direct answers won't help you learn. Let's try a different approach:",
                "suggestions": [
                    "Tell me your understanding of this problem",
                    "Share the methods you've already tried",
                    "Describe the specific difficulties you're facing",
                    "We can analyze the key points of the problem together"
                ]
            },
            ViolationType.HOMEWORK_DOING: {
                "message": "I can't help you complete assignments directly, but I can teach you how to think and solve problems:",
                "suggestions": [
                    "We can analyze the assignment requirements and objectives",
                    "Discuss problem-solving methods and approaches",
                    "Practice related concepts and skills",
                    "Create a study plan to improve your abilities"
                ]
            },
            ViolationType.PLAGIARISM_REQUEST: {
                "message": "Academic integrity is very important. Let me help you learn how to properly cite and express your own ideas:",
                "suggestions": [
                    "Learn how to properly cite sources",
                    "Practice expressing your views in your own words",
                    "Understand academic writing standards",
                    "Develop critical thinking skills"
                ]
            },
            ViolationType.EXCESSIVE_USAGE: {
                "message": "I notice you're using the AI assistant quite frequently. Let's make sure you're learning rather than depending on it:",
                "suggestions": [
                    "Try thinking about problems independently first",
                    "Discuss and exchange ideas with classmates",
                    "Consult relevant learning materials",
                    "Create a reasonable study plan"
                ]
            }
        }
    
    def generate_intervention(self, violation_type: ViolationType, 
                           user_context: Dict = None) -> Dict:
        """生成教育干预内容"""
        intervention = self.intervention_messages.get(violation_type, {
            "message": "让我们以正确的方式使用AI助手来学习。",
            "suggestions": ["思考你的学习目标", "提出具体的问题", "积极参与学习过程"]
        })
        
        return {
            "type": "educational_intervention",
            "violation_type": violation_type.value,
            "message": intervention["message"],
            "suggestions": intervention["suggestions"],
            "timestamp": datetime.now().isoformat(),
            "user_context": user_context
        }


class AIGuardrailSystem:
    """AI护栏系统主类"""
    
    def __init__(self):
        self.content_filter = ContentFilter()
        self.usage_monitor = UsageMonitor()
        self.intervention = EducationalIntervention()
    
    def check_query(self, user_id: int, query: str, context: Dict = None) -> Dict:
        """检查查询并返回处理结果"""
        # 记录查询
        self.usage_monitor.record_query(user_id, query)
        
        # 检查内容违规
        violations = self.content_filter.check_query(query)
        
        # 检查使用频率
        if self.usage_monitor.check_usage_frequency(user_id):
            violations.append((ViolationType.EXCESSIVE_USAGE, 2))
        
        # 检查用户是否应该被限制
        if self.usage_monitor.should_restrict_user(user_id):
            return {
                "allowed": False,
                "reason": "用户因多次违规被暂时限制使用AI助手",
                "action": "restrict",
                "message": "由于多次违反使用规范，你的AI助手访问已被暂时限制。请联系管理员或等待限制解除。",
                "suggestions": ["联系管理员", "查看使用规范", "等待限制解除"]
            }
        
        # 如果有违规，生成干预
        if violations:
            # 记录违规
            for violation_type, severity in violations:
                violation_record = ViolationRecord(
                    user_id=user_id,
                    violation_type=violation_type,
                    query=query,
                    timestamp=datetime.now(),
                    severity=severity,
                    action_taken="educational_intervention",
                    context=context
                )
                self.usage_monitor.record_violation(violation_record)
            
            # 生成教育干预
            intervention = self.intervention.generate_intervention(
                violations[0][0], context
            )
            
            return {
                "allowed": False,
                "reason": f"检测到{len(violations)}个潜在问题",
                "action": "intervention",
                "intervention": intervention,
                "violations": [v[0].value for v in violations]
            }
        
        # 查询通过检查
        return {
            "allowed": True,
            "reason": "查询通过所有检查",
            "action": "proceed"
        }
    
    def get_user_report(self, user_id: int) -> Dict:
        """获取用户使用报告"""
        stats = self.usage_monitor.get_user_stats(user_id)
        violations = self.usage_monitor.get_user_violations(user_id)
        
        return {
            "user_id": user_id,
            "usage_stats": stats,
            "violations": [
                {
                    "type": v.violation_type.value,
                    "timestamp": v.timestamp.isoformat(),
                    "severity": v.severity,
                    "action": v.action_taken
                }
                for v in violations
            ],
            "total_violations": len(violations),
            "is_restricted": self.usage_monitor.should_restrict_user(user_id),
            "recommendations": self._generate_recommendations(stats, violations)
        }
    
    def _generate_recommendations(self, stats: Dict, violations: List[ViolationRecord]) -> List[str]:
        """生成个性化建议"""
        recommendations = []
        
        if stats["average_daily"] > 10:
            recommendations.append("建议减少AI助手使用频率，多尝试独立思考")
        
        if len(violations) > 0:
            recommendations.append("建议仔细阅读AI使用规范，确保负责任使用")
        
        if stats["recent_queries"] > 5:
            recommendations.append("建议制定学习计划，减少对AI的依赖")
        
        if not recommendations:
            recommendations.append("继续保持良好的AI使用习惯")
        
        return recommendations
    
    def get_system_stats(self) -> Dict:
        """获取系统统计信息"""
        total_users = len(self.usage_monitor.user_usage)
        total_violations = len(self.usage_monitor.violation_records)
        
        # 按类型统计违规
        violation_types = {}
        for record in self.usage_monitor.violation_records:
            vtype = record.violation_type.value
            violation_types[vtype] = violation_types.get(vtype, 0) + 1
        
        return {
            "total_users": total_users,
            "total_violations": total_violations,
            "violation_types": violation_types,
            "system_health": "healthy" if total_violations < total_users * 0.1 else "needs_attention"
        }


# 全局护栏系统实例
guardrail_system = AIGuardrailSystem()
