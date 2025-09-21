import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Progress } from '../components/ui/progress';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import {
  Clock,
  BookOpen,
  CheckCircle,
  User,
  Mail,
  Phone,
  Video,
  FileText,
  Download,
  MessageSquare,
  BarChart3,
  Calculator,
  Users,
  MapPin,
  ChevronDown,
  ChevronUp,
  Upload,
  Calendar,
  Grid3X3,
  Sparkles,
} from 'lucide-react';

const courseData = {
  id: 1,
  name: 'Mathematics',
  code: 'MATH 301',
  semester: 'Fall 2024',
  credits: 3,
  description: 'Advanced topics in calculus, linear algebra, and differential equations.',
  professor: {
    name: 'Dr. Sarah Johnson',
    email: 's.johnson@university.edu',
    phone: '+1 (555) 123-4567',
    office: 'Math Building, Room 205',
    officeHours: 'Mon/Wed 2-4 PM',
    zoomLink: 'https://zoom.us/j/123456789',
    avatar: '/placeholder.svg?height=64&width=64',
  },
};

const upcomingTasks = [
  {
    id: 1,
    title: 'Calculus Problem Set #8',
    type: 'assignment',
    dueDate: '2024-03-15',
    dueTime: '11:59 PM',
    status: 'pending',
    points: 100,
    aiComment: 'High Occurrence in tests',
  },
  {
    id: 2,
    title: 'Midterm Exam',
    type: 'exam',
    dueDate: '2024-03-18',
    dueTime: '10:00 AM',
    status: 'upcoming',
    points: 200,
    aiComment: 'Time Consuming',
  },
  {
    id: 3,
    title: 'Linear Algebra Quiz',
    type: 'quiz',
    dueDate: '2024-03-20',
    dueTime: '2:00 PM',
    status: 'upcoming',
    points: 50,
    aiComment: 'Practice Recommended',
  },
];

const modules = [
  {
    id: 1,
    title: 'Differential Calculus',
    progress: 100,
    lessons: 8,
    completed: 8,
    status: 'completed',
  },
  {
    id: 2,
    title: 'Integral Calculus',
    progress: 75,
    lessons: 6,
    completed: 4,
    status: 'in-progress',
  },
  {
    id: 3,
    title: 'Linear Algebra',
    progress: 30,
    lessons: 10,
    completed: 3,
    status: 'in-progress',
  },
  {
    id: 4,
    title: 'Differential Equations',
    progress: 0,
    lessons: 8,
    completed: 0,
    status: 'locked',
  },
];

const resources = [
  { id: 1, name: 'Course Syllabus', type: 'pdf', size: '2.3 MB' },
  { id: 2, name: 'Textbook: Advanced Calculus', type: 'pdf', size: '45.2 MB' },
  { id: 3, name: 'Formula Sheet', type: 'pdf', size: '1.1 MB' },
  { id: 4, name: 'Practice Problems', type: 'pdf', size: '8.7 MB' },
];

const attendanceData = [
  { date: '2024-03-01', status: 'present' },
  { date: '2024-03-04', status: 'present' },
  { date: '2024-03-06', status: 'absent' },
  { date: '2024-03-08', status: 'present' },
  { date: '2024-03-11', status: 'present' },
  { date: '2024-03-13', status: 'late' },
];

const grades = [
  { assignment: 'Problem Set #1', score: 95, total: 100, weight: '10%' },
  { assignment: 'Problem Set #2', score: 88, total: 100, weight: '10%' },
  { assignment: 'Quiz #1', score: 42, total: 50, weight: '5%' },
  { assignment: 'Problem Set #3', score: 92, total: 100, weight: '10%' },
  { assignment: 'Midterm Exam', score: null, total: 200, weight: '25%' },
];

const discussions = [
  {
    id: 1,
    title: 'Question about Integration by Parts',
    author: 'Alex Chen',
    replies: 3,
    lastActivity: '2 hours ago',
    isAnswered: true,
  },
  {
    id: 2,
    title: 'Study Group for Midterm',
    author: 'Maria Rodriguez',
    replies: 8,
    lastActivity: '5 hours ago',
    isAnswered: false,
  },
  {
    id: 3,
    title: 'Clarification on Problem Set #7',
    author: 'John Smith',
    replies: 1,
    lastActivity: '1 day ago',
    isAnswered: true,
  },
];

const CoursePage: React.FC = () => {
  const [viewMode, setViewMode] = useState<'topics' | 'weeks'>('topics');
  const [expandedModules, setExpandedModules] = useState<number[]>([]);

  const getTaskTypeColor = (type: string) => {
    switch (type) {
      case 'assignment':
        return 'bg-blue-500';
      case 'exam':
        return 'bg-red-500';
      case 'quiz':
        return 'bg-green-500';
      case 'project':
        return 'bg-purple-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'present':
        return 'bg-green-500';
      case 'absent':
        return 'bg-red-500';
      case 'late':
        return 'bg-orange-500';
      default:
        return 'bg-gray-500';
    }
  };

  const calculateOverallGrade = () => {
    const completedGrades = grades.filter((g) => g.score !== null);
    const totalPoints = completedGrades.reduce((sum, g) => sum + g.score, 0);
    const maxPoints = completedGrades.reduce((sum, g) => sum + g.total, 0);
    return Math.round((totalPoints / maxPoints) * 100);
  };

  const toggleModuleDropdown = (moduleId: number) => {
    setExpandedModules((prev) =>
      prev.includes(moduleId) ? prev.filter((id) => id !== moduleId) : [...prev, moduleId]
    );
  };

  const enhancedModules = modules.map((module) => ({
    ...module,
    description:
      module.id === 1
        ? 'Fundamental concepts of derivatives, limits, and continuity. Master the basic rules of differentiation.'
        : module.id === 2
          ? 'Integration techniques including substitution, integration by parts, and applications.'
          : module.id === 3
            ? 'Matrix operations, vector spaces, eigenvalues, and linear transformations.'
            : 'First and second-order differential equations with real-world applications.',
    materials:
      module.id === 1
        ? ['Calculus Textbook Ch. 1-3', 'Derivative Rules Sheet', 'Practice Problems']
        : module.id === 2
          ? ['Integration Techniques Guide', 'Practice Integrals', 'Application Examples']
          : module.id === 3
            ? ['Linear Algebra Notes', 'Matrix Calculator', 'Vector Worksheets']
            : ['DE Textbook Ch. 4-6', 'Solution Methods Guide', 'Application Cases'],
    assignments:
      module.id === 1
        ? ['Problem Set #1', 'Derivatives Quiz']
        : module.id === 2
          ? ['Integration Assignment', 'Applications Project']
          : module.id === 3
            ? ['Matrix Quiz', 'Linear Systems Project']
            : ['DE Problem Set', 'Modeling Assignment'],
  }));

  return (
    <div className="space-y-6">
      {/* Course Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
            <Calculator className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-foreground">{courseData.name}</h1>
            <p className="text-muted-foreground">
              {courseData.code} • {courseData.semester} • {courseData.credits} Credits
            </p>
          </div>
        </div>
        <p className="text-muted-foreground max-w-2xl">{courseData.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-3 space-y-6">
          {/* Upcoming Tasks */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <Clock className="w-5 h-5" />
                Upcoming Tasks
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {upcomingTasks.map((task) => (
                <div key={task.id} className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                  <div className={`w-3 h-3 rounded-full ${getTaskTypeColor(task.type)}`} />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <Link to={`/task/${task.id}`} className="hover:underline">
                        <span className="font-medium text-card-foreground cursor-pointer">{task.title}</span>
                      </Link>
                      <Badge variant="outline" className="text-xs capitalize">
                        {task.type}
                      </Badge>
                      <Badge variant="secondary" className="text-xs">
                        {task.points} pts
                      </Badge>
                      <div className="flex items-center gap-1 px-2 py-1 bg-purple-100 dark:bg-purple-900/30 rounded-full">
                        <Sparkles className="w-3 h-3 text-purple-600 dark:text-purple-400" />
                        <span className="text-xs text-purple-700 dark:text-purple-300">{task.aiComment}</span>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Due: {new Date(task.dueDate).toLocaleDateString()} at {task.dueTime}
                    </p>
                  </div>
                  {task.status === 'completed' ? (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  ) : (
                    <Link to={`/task/${task.id}#submission`}>
                      <Upload className="w-5 h-5 text-blue-500 cursor-pointer hover:text-blue-600" />
                    </Link>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Course Modules */}
          <Card className="bg-card border-border">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 text-card-foreground">
                  <BookOpen className="w-5 h-5" />
                  Course Modules
                </CardTitle>
                <div className="flex gap-2">
                  <Button
                    variant={viewMode === 'topics' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setViewMode('topics')}
                    className="gap-2"
                  >
                    <Grid3X3 className="w-4 h-4" />
                    Topics View
                  </Button>
                  <Button
                    variant={viewMode === 'weeks' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setViewMode('weeks')}
                    className="gap-2"
                  >
                    <Calendar className="w-4 h-4" />
                    Weeks View
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {enhancedModules.map((module) => (
                  <div key={module.id} className="p-4 rounded-lg bg-muted/50 border">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-card-foreground">{module.title}</h3>
                      <div className="flex items-center gap-2">
                        <Badge
                          variant={
                            module.status === 'completed'
                              ? 'default'
                              : module.status === 'in-progress'
                                ? 'secondary'
                                : 'outline'
                          }
                        >
                          {module.status === 'completed'
                            ? 'Completed'
                            : module.status === 'in-progress'
                              ? 'In Progress'
                              : 'Locked'}
                        </Badge>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleModuleDropdown(module.id)}
                          className="p-1 h-6 w-6"
                        >
                          {expandedModules.includes(module.id) ? (
                            <ChevronUp className="w-4 h-4" />
                          ) : (
                            <ChevronDown className="w-4 h-4" />
                          )}
                        </Button>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 mb-3">
                      <div className="flex-1">
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-muted-foreground">
                            {module.completed}/{module.lessons} lessons
                          </span>
                          <span className="text-card-foreground">{module.progress}%</span>
                        </div>
                        <Progress value={module.progress} className="h-2" />
                      </div>
                      <Button variant="outline" size="sm" disabled={module.status === 'locked'}>
                        {module.status === 'completed' ? 'Review' : 'Continue'}
                      </Button>
                    </div>

                    {expandedModules.includes(module.id) && (
                      <div className="mt-4 pt-4 border-t border-border space-y-4">
                        <div>
                          <h4 className="font-medium text-card-foreground mb-2">Description</h4>
                          <p className="text-sm text-muted-foreground">{module.description}</p>
                        </div>

                        <div>
                          <h4 className="font-medium text-card-foreground mb-2">Materials</h4>
                          <div className="space-y-2">
                            {module.materials.map((material, index) => (
                              <div key={index} className="flex items-center gap-2 text-sm">
                                <FileText className="w-4 h-4 text-muted-foreground" />
                                <span className="text-card-foreground">{material}</span>
                                <Button variant="ghost" size="sm" className="ml-auto p-1 h-6">
                                  <Download className="w-3 h-3" />
                                </Button>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h4 className="font-medium text-card-foreground mb-2">Assignments</h4>
                          <div className="space-y-3">
                            {module.assignments.map((assignment, index) => (
                              <div key={index} className="p-3 bg-background rounded-lg border">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="text-sm font-medium text-card-foreground">{assignment}</span>
                                  <Badge variant="outline" className="text-xs">
                                    Due Soon
                                  </Badge>
                                </div>
                                <div className="flex items-center gap-2">
                                  <Button variant="outline" size="sm" className="gap-2 bg-transparent">
                                    <Upload className="w-3 h-3" />
                                    Submit
                                  </Button>
                                  <Button variant="ghost" size="sm">
                                    View Details
                                  </Button>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Course Resources */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <FileText className="w-5 h-5" />
                Course Resources
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {resources.map((resource) => (
                <div key={resource.id} className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                  <FileText className="w-5 h-5 text-muted-foreground" />
                  <div className="flex-1">
                    <span className="font-medium text-card-foreground">{resource.name}</span>
                    <p className="text-sm text-muted-foreground">
                      {resource.type.toUpperCase()} • {resource.size}
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Discussion Forum */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <MessageSquare className="w-5 h-5" />
                Discussion Forum
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {discussions.map((discussion) => (
                <div key={discussion.id} className="p-3 rounded-lg bg-muted/50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium text-card-foreground">{discussion.title}</span>
                        {discussion.isAnswered && (
                          <Badge variant="default" className="text-xs">
                            Answered
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        by {discussion.author} • {discussion.replies} replies • {discussion.lastActivity}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              <Button variant="outline" className="w-full bg-transparent">
                <MessageSquare className="w-4 h-4 mr-2" />
                Start New Discussion
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Professor Info */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <User className="w-5 h-5" />
                Professor
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-3">
                <Avatar className="h-12 w-12">
                  <AvatarImage src={courseData.professor.avatar || '/placeholder.svg'} alt={courseData.professor.name} />
                  <AvatarFallback>SJ</AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="font-medium text-card-foreground">{courseData.professor.name}</h3>
                  <p className="text-sm text-muted-foreground">Course Instructor</p>
                </div>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4 text-muted-foreground" />
                  <span className="text-card-foreground">{courseData.professor.email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4 text-muted-foreground" />
                  <span className="text-card-foreground">{courseData.professor.phone}</span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-muted-foreground" />
                  <span className="text-card-foreground">{courseData.professor.office}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <span className="text-card-foreground">{courseData.professor.officeHours}</span>
                </div>
              </div>

              <Button className="w-full gap-2">
                <Video className="w-4 h-4" />
                Join Office Hours
              </Button>
            </CardContent>
          </Card>

          {/* Grades Overview */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <BarChart3 className="w-5 h-5" />
                Grades
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-card-foreground">{calculateOverallGrade()}%</div>
                <p className="text-sm text-muted-foreground">Overall Grade</p>
              </div>

              <div className="space-y-2">
                {grades.map((grade, index) => (
                  <div key={index} className="flex justify-between items-center text-sm">
                    <span className="text-muted-foreground truncate">{grade.assignment}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-card-foreground">
                        {grade.score !== null ? `${grade.score}/${grade.total}` : 'Pending'}
                      </span>
                      <Badge variant="outline" className="text-xs">
                        {grade.weight}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Attendance */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <Users className="w-5 h-5" />
                Attendance
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4 p-3 bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-orange-500" />
                  <span className="text-sm font-medium text-orange-800 dark:text-orange-200">
                    You can only skip 5 more classes to not lose 10% of your GPA
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-6 gap-2">
                {attendanceData.map((record, index) => (
                  <div
                    key={index}
                    className={`w-6 h-6 rounded-full ${getStatusColor(record.status)}`}
                    title={`${record.date}: ${record.status}`}
                  />
                ))}
              </div>
              <div className="flex justify-between text-xs text-muted-foreground mt-3">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                  Present
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-orange-500" />
                  Late
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-red-500" />
                  Absent
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default CoursePage;
