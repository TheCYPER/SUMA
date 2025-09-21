import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  BookOpenIcon, 
  ClipboardDocumentListIcon, 
  CalendarIcon,
  AcademicCapIcon 
} from '@heroicons/react/24/outline';
import apiService from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard: React.FC = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: apiService.getDashboardStats,
  });

  const { data: upcomingTasks } = useQuery({
    queryKey: ['upcoming-tasks'],
    queryFn: apiService.getUpcomingTasks,
  });

  if (isLoading) {
    return <LoadingSpinner size="lg" className="mt-8" />;
  }

  const statCards = [
    {
      name: '总课程数',
      value: stats?.total_courses || 0,
      icon: BookOpenIcon,
      color: 'bg-blue-500',
    },
    {
      name: '总任务数',
      value: stats?.total_tasks || 0,
      icon: ClipboardDocumentListIcon,
      color: 'bg-green-500',
    },
    {
      name: '即将到期',
      value: stats?.upcoming_tasks || 0,
      icon: CalendarIcon,
      color: 'bg-yellow-500',
    },
    {
      name: '已完成',
      value: stats?.completed_tasks || 0,
      icon: AcademicCapIcon,
      color: 'bg-purple-500',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">仪表板</h1>
        <p className="mt-1 text-sm text-gray-500">
          欢迎回来！这里是您的学习概览。
        </p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => (
          <div key={card.name} className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${card.color}`}>
                  <card.icon className="w-6 h-6 text-white" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{card.name}</p>
                  <p className="text-2xl font-semibold text-gray-900">{card.value}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* 即将到期的任务 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">即将到期的任务</h3>
          </div>
          <div className="card-body">
            {upcomingTasks && upcomingTasks.length > 0 ? (
              <div className="space-y-3">
                {upcomingTasks.slice(0, 5).map((task) => (
                  <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{task.title}</p>
                      <p className="text-xs text-gray-500">{task.course.name}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-500">
                        {new Date(task.due_date).toLocaleDateString()}
                      </p>
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        {task.points} 分
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">暂无即将到期的任务</p>
            )}
          </div>
        </div>

        {/* 最近活动 */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">最近活动</h3>
          </div>
          <div className="card-body">
            {stats?.recent_activities && stats.recent_activities.length > 0 ? (
              <div className="space-y-3">
                {stats.recent_activities.slice(0, 5).map((activity) => (
                  <div key={activity.id} className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-900">{activity.description}</p>
                      <p className="text-xs text-gray-500">
                        {new Date(activity.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">暂无最近活动</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
