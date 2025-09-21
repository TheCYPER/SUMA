// 用户相关类型
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: 'student' | 'teacher' | 'admin';
  theme: string;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// 课程相关类型
export interface Course {
  id: number;
  name: string;
  description: string;
  icon: string;
  color: string;
  teacher_id: number;
  teacher: User;
  created_at: string;
  updated_at: string;
  enrolled?: boolean;
  student_count?: number;
}

export interface CreateCourseRequest {
  name: string;
  description: string;
  icon: string;
  color: string;
}

// 任务相关类型
export interface Task {
  id: number;
  title: string;
  description: string;
  task_type: 'assignment' | 'test' | 'lab' | 'project' | 'quiz';
  points: number;
  due_date: string;
  course_id: number;
  course: Course;
  created_at: string;
  updated_at: string;
  status?: 'not_started' | 'in_progress' | 'submitted' | 'graded';
  submission?: TaskSubmission;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  task_type: 'assignment' | 'test' | 'lab' | 'project' | 'quiz';
  points: number;
  due_date: string;
  course_id: number;
}

export interface TaskSubmission {
  id: number;
  task_id: number;
  student_id: number;
  content: string;
  grade?: number;
  feedback?: string;
  submitted_at: string;
  graded_at?: string;
  attachments: FileAttachment[];
}

export interface CreateSubmissionRequest {
  content: string;
  attachments?: File[];
}

// 文件相关类型
export interface FileAttachment {
  id: number;
  filename: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  uploaded_at: string;
}

// 日历相关类型
export interface CalendarEvent {
  id: number;
  title: string;
  description: string;
  start_time: string;
  end_time: string;
  event_type: 'task' | 'event' | 'deadline';
  course_id?: number;
  task_id?: number;
  created_at: string;
}

export interface CreateEventRequest {
  title: string;
  description: string;
  start_time: string;
  end_time: string;
  event_type: 'task' | 'event' | 'deadline';
  course_id?: number;
  task_id?: number;
}

// AI相关类型
export interface AIQuery {
  query: string;
  context?: string;
}

export interface AIResponse {
  response: string;
  agent_type: string;
  suggestions?: string[];
}

export interface AIAgent {
  id: string;
  name: string;
  description: string;
  capabilities: string[];
}

// 仪表板相关类型
export interface DashboardStats {
  total_courses: number;
  total_tasks: number;
  upcoming_tasks: number;
  completed_tasks: number;
  average_grade: number;
  recent_activities: Activity[];
}

export interface Activity {
  id: number;
  type: string;
  description: string;
  timestamp: string;
  course_id?: number;
  task_id?: number;
}

// API响应类型
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// 错误类型
export interface ApiError {
  detail: string;
  status_code: number;
}

// 表单类型
export interface FormState {
  isLoading: boolean;
  error: string | null;
  success: boolean;
}
