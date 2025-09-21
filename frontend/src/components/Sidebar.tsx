import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  HomeIcon,
  BookOpenIcon,
  ClipboardDocumentListIcon,
  CalendarIcon,
  ChatBubbleLeftRightIcon,
  UserGroupIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';

const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const location = useLocation();

  const navigation = [
    { name: '仪表板', href: '/', icon: HomeIcon },
    { name: '课程', href: '/courses', icon: BookOpenIcon },
    { name: '任务', href: '/tasks', icon: ClipboardDocumentListIcon },
    { name: '日历', href: '/calendar', icon: CalendarIcon },
    { name: 'AI助手', href: '/ai', icon: ChatBubbleLeftRightIcon },
  ];

  // 根据用户角色添加管理功能
  if (user?.role === 'admin' || user?.role === 'teacher') {
    navigation.push(
      { name: '用户管理', href: '/users', icon: UserGroupIcon },
      { name: '设置', href: '/settings', icon: Cog6ToothIcon }
    );
  }

  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
      <div className="p-6">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">S</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">SUMA</h2>
            <p className="text-xs text-gray-500">学习管理系统</p>
          </div>
        </div>
      </div>
      
      <nav className="mt-6">
        <div className="px-3 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                  isActive
                    ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <item.icon
                  className={`mr-3 h-5 w-5 ${
                    isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-500'
                  }`}
                />
                {item.name}
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;
