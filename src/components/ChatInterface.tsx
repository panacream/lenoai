
import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Send, 
  Bot, 
  User, 
  Loader2, 
  AlertCircle, 
  CheckCircle,
  Code,
  Coins,
  Users,
  Mail,
  Globe
} from 'lucide-react';

const agentIcons = {
  manager: Bot,
  coding: Code,
  token: Coins,
  social: Users,
  google: Mail,
  scraper: Globe
};

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  agent?: string;
  timestamp: Date;
  status: 'sent' | 'processing' | 'completed' | 'error';
}

interface ChatInterfaceProps {
  sessionData: any;
  onSessionUpdate: (data: any) => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
  sessionData, 
  onSessionUpdate 
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Hello! I\'m the Manager Agent. I can help you with various tasks across multiple domains. What would you like to do today?',
      sender: 'agent',
      agent: 'manager',
      timestamp: new Date(),
      status: 'completed'
    }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isProcessing) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      sender: 'user',
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    // Simulate agent processing
    setTimeout(() => {
      const agentResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: simulateAgentResponse(input),
        sender: 'agent',
        agent: determineAgent(input),
        timestamp: new Date(),
        status: 'completed'
      };

      setMessages(prev => [...prev, agentResponse]);
      setIsProcessing(false);
    }, 2000);
  };

  const simulateAgentResponse = (userInput: string): string => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('code') || lowerInput.includes('github')) {
      return 'I\'ve delegated your request to the Coding Agent. It can help with GitHub operations, code generation, and repository management. What specific coding task would you like to accomplish?';
    } else if (lowerInput.includes('token') || lowerInput.includes('wallet')) {
      return 'Routing your request to the Token Agent. It handles LENOAI token operations including balance checks, transfers, minting, and burning. What token operation would you like to perform?';
    } else if (lowerInput.includes('linkedin') || lowerInput.includes('social')) {
      return 'Connecting you with the Social Media Agent. It can manage LinkedIn posts, profile updates, and event handling. What social media task can I help you with?';
    } else if (lowerInput.includes('email') || lowerInput.includes('gmail')) {
      return 'Forwarding to the Google Agent for email, calendar, and spreadsheet operations. What Google service integration do you need?';
    } else if (lowerInput.includes('scrape') || lowerInput.includes('data')) {
      return 'Activating the Scraper Agent for web scraping and data extraction tasks. Please provide the URL or data source you\'d like to scrape.';
    } else {
      return 'I understand your request. Let me analyze the best approach and delegate to the appropriate specialist agent. Could you provide more specific details about what you\'d like to accomplish?';
    }
  };

  const determineAgent = (userInput: string): string => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('code') || lowerInput.includes('github')) return 'coding';
    if (lowerInput.includes('token') || lowerInput.includes('wallet')) return 'token';
    if (lowerInput.includes('linkedin') || lowerInput.includes('social')) return 'social';
    if (lowerInput.includes('email') || lowerInput.includes('gmail')) return 'google';
    if (lowerInput.includes('scrape') || lowerInput.includes('data')) return 'scraper';
    
    return 'manager';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'processing':
        return <Loader2 className="w-3 h-3 animate-spin text-blue-500" />;
      case 'completed':
        return <CheckCircle className="w-3 h-3 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-3 h-3 text-red-500" />;
      default:
        return null;
    }
  };

  const getAgentIcon = (agent?: string) => {
    if (!agent) return User;
    const IconComponent = agentIcons[agent as keyof typeof agentIcons] || Bot;
    return IconComponent;
  };

  return (
    <div className="max-w-4xl mx-auto">
      <Card className="h-[600px] flex flex-col">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Bot className="w-5 h-5" />
            <span>Multi-Agent Chat Interface</span>
            {isProcessing && (
              <Badge variant="secondary" className="ml-auto">
                <Loader2 className="w-3 h-3 animate-spin mr-1" />
                Processing
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col space-y-4">
          <ScrollArea className="flex-1 pr-4" ref={scrollAreaRef}>
            <div className="space-y-4">
              {messages.map((message) => {
                const IconComponent = message.sender === 'user' 
                  ? User 
                  : getAgentIcon(message.agent);
                
                return (
                  <div
                    key={message.id}
                    className={`flex items-start space-x-3 ${
                      message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                    }`}
                  >
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.sender === 'user' 
                        ? 'bg-blue-500' 
                        : 'bg-green-500'
                    }`}>
                      <IconComponent className="w-4 h-4 text-white" />
                    </div>
                    <div className={`flex-1 ${
                      message.sender === 'user' ? 'text-right' : ''
                    }`}>
                      <div className={`inline-block max-w-xs lg:max-w-md xl:max-w-lg rounded-lg px-4 py-2 ${
                        message.sender === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}>
                        <p className="text-sm">{message.content}</p>
                      </div>
                      <div className={`flex items-center space-x-2 mt-1 text-xs text-gray-500 ${
                        message.sender === 'user' ? 'justify-end' : ''
                      }`}>
                        <span>{message.timestamp.toLocaleTimeString()}</span>
                        {message.agent && (
                          <Badge variant="outline" className="text-xs">
                            {message.agent}
                          </Badge>
                        )}
                        {getStatusIcon(message.status)}
                      </div>
                    </div>
                  </div>
                );
              })}
              {isProcessing && (
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
                    <Loader2 className="w-4 h-4 animate-spin text-gray-600" />
                  </div>
                  <div className="bg-gray-100 rounded-lg px-4 py-2">
                    <p className="text-sm text-gray-600">Agent is thinking...</p>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
          
          <div className="flex space-x-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask any agent to help you with tasks..."
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              disabled={isProcessing}
              className="flex-1"
            />
            <Button 
              onClick={handleSend} 
              disabled={!input.trim() || isProcessing}
              className="bg-blue-500 hover:bg-blue-600"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
