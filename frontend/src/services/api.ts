import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  User,
  LoginRequest,
  LoginResponse,
  Course,
  CreateCourseRequest,
  Task,
  CreateTaskRequest,
  TaskSubmission,
  CreateSubmissionRequest,
  CalendarEvent,
  CreateEventRequest,
  AIQuery,
  AIResponse,
  DashboardStats,
  ApiResponse,
  PaginatedResponse
} from '../types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: 'http://localhost:8000/api/v1',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器 - 添加认证token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器 - 处理错误
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token过期，清除本地存储并跳转到登录页
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // 认证相关
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response: AxiosResponse<LoginResponse> = await this.api.post('/auth/login-json', credentials);
    return response.data;
  }

  async register(userData: any): Promise<User> {
    const response: AxiosResponse<User> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/auth/me');
    return response.data;
  }

  // 课程相关
  async getCourses(): Promise<Course[]> {
    const response: AxiosResponse<Course[]> = await this.api.get('/courses/');
    return response.data;
  }

  async getCourse(id: number): Promise<Course> {
    const response: AxiosResponse<Course> = await this.api.get(`/courses/${id}`);
    return response.data;
  }

  async createCourse(courseData: CreateCourseRequest): Promise<Course> {
    const response: AxiosResponse<Course> = await this.api.post('/courses/', courseData);
    return response.data;
  }

  async enrollInCourse(courseId: number): Promise<void> {
    await this.api.post(`/courses/${courseId}/enroll`);
  }

  // 任务相关
  async getTasks(): Promise<Task[]> {
    const response: AxiosResponse<Task[]> = await this.api.get('/tasks/');
    return response.data;
  }

  async getUpcomingTasks(): Promise<Task[]> {
    const response: AxiosResponse<Task[]> = await this.api.get('/tasks/upcoming');
    return response.data;
  }

  async getTask(id: number): Promise<Task> {
    const response: AxiosResponse<Task> = await this.api.get(`/tasks/${id}`);
    return response.data;
  }

  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    const response: AxiosResponse<Task> = await this.api.post('/tasks/', taskData);
    return response.data;
  }

  async submitTask(taskId: number, submissionData: CreateSubmissionRequest): Promise<TaskSubmission> {
    const formData = new FormData();
    formData.append('content', submissionData.content);
    
    if (submissionData.attachments) {
      submissionData.attachments.forEach((file, index) => {
        formData.append(`attachments`, file);
      });
    }

    const response: AxiosResponse<TaskSubmission> = await this.api.post(
      `/tasks/${taskId}/submission`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  // 日历相关
  async getCalendarEvents(): Promise<CalendarEvent[]> {
    const response: AxiosResponse<CalendarEvent[]> = await this.api.get('/calendar/events');
    return response.data;
  }

  async createEvent(eventData: CreateEventRequest): Promise<CalendarEvent> {
    const response: AxiosResponse<CalendarEvent> = await this.api.post('/calendar/events', eventData);
    return response.data;
  }

  async exportCalendar(): Promise<Blob> {
    const response: AxiosResponse<Blob> = await this.api.get('/calendar/export/ics', {
      responseType: 'blob',
    });
    return response.data;
  }

  // 仪表板相关
  async getDashboardStats(): Promise<DashboardStats> {
    const response: AxiosResponse<DashboardStats> = await this.api.get('/calendar/dashboard');
    return response.data;
  }

  // AI相关
  async queryAI(query: AIQuery): Promise<AIResponse> {
    const response: AxiosResponse<AIResponse> = await this.api.post('/ai/query', query);
    return response.data;
  }

  async getAIStatus(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/ai/status');
    return response.data;
  }

  async getStudyTips(): Promise<string[]> {
    const response: AxiosResponse<string[]> = await this.api.get('/ai/study-tips');
    return response.data;
  }

  // 文件相关
  async uploadFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const response: AxiosResponse<any> = await this.api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async downloadFile(path: string): Promise<Blob> {
    const response: AxiosResponse<Blob> = await this.api.get(`/files/download/${path}`, {
      responseType: 'blob',
    });
    return response.data;
  }

  async previewFile(path: string): Promise<string> {
    const response: AxiosResponse<string> = await this.api.get(`/files/preview/${path}`);
    return response.data;
  }
}

// 创建单例实例
export const apiService = new ApiService();
export default apiService;
