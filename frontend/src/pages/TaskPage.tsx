import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Input } from '../components/ui/input';
import { Separator } from '../components/ui/separator';
import {
  Clock,
  FileText,
  Upload,
  Download,
  Bot,
  Send,
  CheckCircle,
  AlertCircle,
  Calendar,
  Tag,
  BookOpen,
  Paperclip,
  Eye,
  Trash2,
  Sparkles,
} from 'lucide-react';

const taskData = {
  id: 1,
  title: 'Calculus Problem Set #8',
  course: 'Advanced Mathematics',
  courseCode: 'MATH 301',
  type: 'assignment',
  dueDate: '2024-03-15',
  dueTime: '11:59 PM',
  points: 100,
  status: 'pending',
  description: `Complete the following calculus problems focusing on integration techniques and applications. 

**Instructions:**
1. Show all work clearly
2. Use proper mathematical notation
3. Include graphs where applicable
4. Submit as a single PDF file

**Problems to solve:**
- Integration by parts (Problems 1-5)
- Trigonometric substitution (Problems 6-10)
- Partial fractions (Problems 11-15)
- Applications to area and volume (Problems 16-20)

**Grading Criteria:**
- Correct solutions (70%)
- Clear work shown (20%)
- Proper notation (10%)`,
  tags: ['calculus', 'integration', 'problem-solving'],
  attachments: [
    {
      id: 1,
      name: 'Problem_Set_8.pdf',
      size: '2.3 MB',
      type: 'pdf',
      uploadedBy: 'instructor',
    },
    {
      id: 2,
      name: 'Integration_Reference.pdf',
      size: '1.8 MB',
      type: 'pdf',
      uploadedBy: 'instructor',
    },
  ],
};

const submissionHistory = [
  {
    id: 1,
    fileName: 'draft_solution.pdf',
    uploadDate: '2024-03-12',
    uploadTime: '3:45 PM',
    size: '1.2 MB',
    status: 'draft',
  },
];

const TaskPage: React.FC = () => {
  const [submissionText, setSubmissionText] = useState('');
  const [aiQuery, setAiQuery] = useState('');
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [aiResponse, setAiResponse] = useState('');

  const handleAiSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!aiQuery.trim()) return;

    setIsAiLoading(true);
    // Simulate AI response
    setTimeout(() => {
      setAiResponse(
        `Based on the attached Problem Set #8, I can see this assignment focuses on advanced integration techniques. Here's a summary:

**Key Topics:**
- Integration by parts: Use the formula ∫u dv = uv - ∫v du
- Trigonometric substitution: For expressions with √(a²-x²), √(a²+x²), √(x²-a²)
- Partial fractions: Decompose rational functions before integrating
- Applications: Calculate areas between curves and volumes of revolution

**Recommended Approach:**
1. Start with problems 1-5 (integration by parts) as they build foundational skills
2. Review trigonometric identities before tackling problems 6-10
3. Practice partial fraction decomposition separately before problems 11-15
4. Use graphing tools to visualize the applications in problems 16-20

**Study Tips:**
- Keep the integration reference sheet handy
- Double-check your work by differentiating your answers
- Pay attention to constants of integration`,
      );
      setIsAiLoading(false);
      setAiQuery('');
    }, 2000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'submitted':
        return 'text-green-500';
      case 'graded':
        return 'text-blue-500';
      case 'late':
        return 'text-red-500';
      default:
        return 'text-orange-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'submitted':
      case 'graded':
        return <CheckCircle className="w-5 h-5" />;
      default:
        return <AlertCircle className="w-5 h-5" />;
    }
  };

  const daysUntilDue = Math.ceil((new Date(taskData.dueDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));

  return (
    <div className="space-y-6">
      {/* Task Header */}
      <div className="mb-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-foreground">{taskData.title}</h1>
              <div className={`flex items-center gap-1 ${getStatusColor(taskData.status)}`}>
                {getStatusIcon(taskData.status)}
                <span className="capitalize font-medium">{taskData.status}</span>
              </div>
            </div>
            <div className="flex items-center gap-4 text-muted-foreground">
              <div className="flex items-center gap-1">
                <BookOpen className="w-4 h-4" />
                <span>
                  {taskData.course} ({taskData.courseCode})
                </span>
              </div>
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                <span>
                  Due: {new Date(taskData.dueDate).toLocaleDateString()} at {taskData.dueTime}
                </span>
              </div>
              <div className="flex items-center gap-1">
                <Clock className="w-4 h-4" />
                <span className={daysUntilDue <= 1 ? 'text-red-500' : ''}>
                  {daysUntilDue > 0 ? `${daysUntilDue} days left` : 'Overdue'}
                </span>
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-foreground">{taskData.points}</div>
            <div className="text-sm text-muted-foreground">points</div>
          </div>
        </div>

        {/* Tags */}
        <div className="flex items-center gap-2">
          <Tag className="w-4 h-4 text-muted-foreground" />
          {taskData.tags.map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Task Description */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <FileText className="w-5 h-5" />
                Task Description
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none text-card-foreground">
                <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed">{taskData.description}</pre>
              </div>
            </CardContent>
          </Card>

          {/* Attachments */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <Paperclip className="w-5 h-5" />
                Attachments
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {taskData.attachments.map((attachment) => (
                <div key={attachment.id} className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                  <FileText className="w-5 h-5 text-muted-foreground" />
                  <div className="flex-1">
                    <span className="font-medium text-card-foreground">{attachment.name}</span>
                    <p className="text-sm text-muted-foreground">
                      {attachment.type.toUpperCase()} • {attachment.size} • Uploaded by {attachment.uploadedBy}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                      <Eye className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* AI Assistant */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                  <Bot className="w-4 h-4 text-primary-foreground" />
                </div>
                AI Task Assistant
                <Badge variant="secondary" className="ml-auto">
                  <Sparkles className="w-3 h-3 mr-1" />
                  Smart Analysis
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <form onSubmit={handleAiSubmit} className="flex gap-2">
                <Input
                  value={aiQuery}
                  onChange={(e) => setAiQuery(e.target.value)}
                  placeholder="Ask about the task requirements, get study tips, or request a summary..."
                  className="flex-1 bg-muted border-0"
                  disabled={isAiLoading}
                />
                <Button type="submit" size="sm" disabled={isAiLoading || !aiQuery.trim()}>
                  <Send className="w-4 h-4" />
                </Button>
              </form>

              {aiResponse && (
                <div className="p-4 rounded-lg bg-muted/50 border-l-4 border-primary">
                  <div className="prose prose-sm max-w-none text-card-foreground">
                    <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed">{aiResponse}</pre>
                  </div>
                </div>
              )}

              <div className="flex flex-wrap gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="text-xs h-7 bg-transparent"
                  onClick={() => setAiQuery('Summarize the task requirements')}
                >
                  Summarize requirements
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="text-xs h-7 bg-transparent"
                  onClick={() => setAiQuery('Give me study tips for this assignment')}
                >
                  Study tips
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="text-xs h-7 bg-transparent"
                  onClick={() => setAiQuery('What are the key concepts I need to know?')}
                >
                  Key concepts
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Submission */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <Upload className="w-5 h-5" />
                Submit Assignment
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-card-foreground mb-2">Upload Files</label>
                <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                  <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                  <p className="text-sm text-muted-foreground mb-2">Drag and drop files here, or click to browse</p>
                  <Button variant="outline" size="sm">
                    Choose Files
                  </Button>
                </div>
              </div>

              {/* Text Submission */}
              <div>
                <label className="block text-sm font-medium text-card-foreground mb-2">
                  Text Submission (Optional)
                </label>
                <Textarea
                  value={submissionText}
                  onChange={(e) => setSubmissionText(e.target.value)}
                  placeholder="Add any additional comments or explanations..."
                  className="min-h-[100px] bg-muted border-0"
                />
              </div>

              {/* Previous Submissions */}
              {submissionHistory.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-card-foreground mb-2">Previous Submissions</h4>
                  <div className="space-y-2">
                    {submissionHistory.map((submission) => (
                      <div key={submission.id} className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                        <FileText className="w-4 h-4 text-muted-foreground" />
                        <div className="flex-1">
                          <span className="font-medium text-card-foreground">{submission.fileName}</span>
                          <p className="text-sm text-muted-foreground">
                            {submission.uploadDate} at {submission.uploadTime} • {submission.size}
                          </p>
                        </div>
                        <Badge variant="outline" className="text-xs capitalize">
                          {submission.status}
                        </Badge>
                        <Button variant="outline" size="sm">
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <Separator />

              <div className="flex justify-between items-center">
                <p className="text-sm text-muted-foreground">Make sure to review your work before submitting</p>
                <div className="flex gap-2">
                  <Button variant="outline">Save Draft</Button>
                  <Button>Submit Assignment</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Task Status */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <CheckCircle className="w-5 h-5" />
                Task Status
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center">
                <div className={`text-2xl font-bold ${getStatusColor(taskData.status)}`}>
                  {taskData.status.charAt(0).toUpperCase() + taskData.status.slice(1)}
                </div>
                <p className="text-sm text-muted-foreground">Current Status</p>
              </div>

              <Separator />

              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Type:</span>
                  <Badge variant="outline" className="capitalize">
                    {taskData.type}
                  </Badge>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Points:</span>
                  <span className="text-card-foreground font-medium">{taskData.points}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Due Date:</span>
                  <span className="text-card-foreground font-medium">
                    {new Date(taskData.dueDate).toLocaleDateString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Due Time:</span>
                  <span className="text-card-foreground font-medium">{taskData.dueTime}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Time Left:</span>
                  <span className={`font-medium ${daysUntilDue <= 1 ? 'text-red-500' : 'text-card-foreground'}`}>
                    {daysUntilDue > 0 ? `${daysUntilDue} days` : 'Overdue'}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-card-foreground">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start bg-transparent">
                <Calendar className="w-4 h-4 mr-2" />
                Add to Calendar
              </Button>
              <Button variant="outline" className="w-full justify-start bg-transparent">
                <Download className="w-4 h-4 mr-2" />
                Download All Files
              </Button>
              <Button variant="outline" className="w-full justify-start bg-transparent">
                <FileText className="w-4 h-4 mr-2" />
                View Rubric
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default TaskPage;
