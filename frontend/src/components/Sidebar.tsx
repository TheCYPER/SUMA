import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import {
  BookOpen,
  Calculator,
  Atom,
  Code,
  Globe,
  Palette,
  FileText,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';

const courses = [
  { id: 1, name: "Mathematics", code: "MATH 301", icon: Calculator, color: "bg-blue-500", progress: 75 },
  { id: 2, name: "Physics", code: "PHYS 201", icon: Atom, color: "bg-green-500", progress: 60 },
  { id: 3, name: "Computer Science", code: "CS 350", icon: Code, color: "bg-purple-500", progress: 85 },
  { id: 4, name: "History", code: "HIST 101", icon: Globe, color: "bg-orange-500", progress: 45 },
  { id: 5, name: "Art", code: "ART 250", icon: Palette, color: "bg-pink-500", progress: 70 },
];

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ collapsed, onToggle }) => {
  const { user } = useAuth();
  const location = useLocation();

  return (
    <div
      className={`bg-sidebar border-r border-sidebar-border transition-all duration-300 ${
        collapsed ? "w-16" : "w-64"
      } flex flex-col sticky top-0 h-screen`}
    >
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                <BookOpen className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="font-semibold text-sidebar-foreground min-w-0 truncate">
                Beijing Etown Academy
              </span>
            </Link>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggle}
            className="text-sidebar-foreground hover:bg-sidebar-accent"
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      {/* Courses */}
      <div className="flex-1 p-4 overflow-y-auto">
        {!collapsed && <h3 className="text-sm font-medium text-sidebar-foreground mb-3">Courses</h3>}
        <div className="space-y-2">
          {courses.map((course) => {
            const Icon = course.icon;
            return (
              <Link key={course.id} to={`/course/${course.id}`}>
                <Button
                  variant="ghost"
                  className={`w-full justify-start text-sidebar-foreground hover:bg-sidebar-accent ${
                    collapsed ? "px-2" : "px-3"
                  }`}
                >
                  <div
                    className={`w-6 h-6 rounded-md ${course.color} flex items-center justify-center mr-3 flex-shrink-0`}
                  >
                    <Icon className="w-3 h-3 text-white" />
                  </div>
                  {!collapsed && (
                    <div className="flex-1 text-left min-w-0">
                      <div className="text-sm truncate">
                        {course.name} <span className="text-xs text-muted-foreground">({course.code})</span>
                      </div>
                      <div className="text-xs text-muted-foreground">{course.progress}% complete</div>
                    </div>
                  )}
                </Button>
              </Link>
            );
          })}
        </div>

        {!collapsed && (
          <>
            <h3 className="text-sm font-medium text-sidebar-foreground mb-3 mt-6">Resources</h3>
            <div className="space-y-2">
              <Button variant="ghost" className="w-full justify-start text-sidebar-foreground hover:bg-sidebar-accent">
                <FileText className="w-4 h-4 mr-3" />
                Textbooks
              </Button>
              <Button variant="ghost" className="w-full justify-start text-sidebar-foreground hover:bg-sidebar-accent">
                <BookOpen className="w-4 h-4 mr-3" />
                Study Guides
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Sidebar;