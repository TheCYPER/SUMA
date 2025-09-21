import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Bot, Send, Sparkles } from 'lucide-react';

export const AIAssistant: React.FC = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    // Simulate AI response
    setTimeout(() => {
      setIsLoading(false);
      setQuery('');
    }, 2000);
  };

  const quickQuestions = [
    'Which task should I review for the quiz?',
    'What are the ten axioms of a vector space',
    'What is the difference between imagry and allusions',
    'Write me a polite message to my professor for an extension',
  ];

  return (
    <Card className="bg-card border-border">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-card-foreground">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <Bot className="w-4 h-4 text-primary-foreground" />
          </div>
          AI Assistant
          <Badge variant="secondary" className="ml-auto">
            <Sparkles className="w-3 h-3 mr-1" />
            Smart
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask me anything about your studies..."
            className="flex-1 bg-muted border-0"
            disabled={isLoading}
          />
          <Button type="submit" size="sm" disabled={isLoading || !query.trim()}>
            <Send className="w-4 h-4" />
          </Button>
        </form>

        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">Quick questions:</p>
          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((question, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                className="text-xs h-7 bg-transparent"
                onClick={() => setQuery(question)}
              >
                {question}
              </Button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AIAssistant;
