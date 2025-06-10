
import React, { useState, useEffect } from 'react';
import AgentChat from '@/components/AgentChat';
import { AgentPanels } from '@/components/AgentPanels';
import { SessionHistory } from '@/components/SessionHistory';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { useAgentChat } from "@/hooks/useAgentChat";
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Bot, MessageCircle, History, Settings } from 'lucide-react';

const Index = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [sessionData, setSessionData] = useState({
    messages: [],
    activeAgent: null,
    isConnected: false
  });
  // Use the agent chat hook at the page level
  const agentChat = useAgentChat();

  useEffect(() => {
    // Initialize session and check backend connectivity
    const initializeSession = async () => {
      try {
        // Simulate backend connection check
        setSessionData(prev => ({ ...prev, isConnected: true }));
      } catch (error) {
        console.error('Failed to connect to agent backend:', error);
      }
    };
    
    initializeSession();
  }, []);

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-green-500 rounded-lg flex items-center justify-center">
                  <Bot className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-slate-900">Leno AI</h1>
                  <p className="text-sm text-slate-600">The Greatest AI For Everything!</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
                  sessionData.isConnected 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  <div className={`w-2 h-2 rounded-full ${
                    sessionData.isConnected ? 'bg-green-500' : 'bg-red-500'
                  }`} />
                  {sessionData.isConnected ? 'Connected' : 'Disconnected'}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-3 lg:w-72">
              <TabsTrigger value="chat">
                <MessageCircle className="w-4 h-4 mr-1" /> Chat
              </TabsTrigger>
              <TabsTrigger value="agents">
                <Bot className="w-4 h-4 mr-1" /> Agents
              </TabsTrigger>
              <TabsTrigger value="history">
                <History className="w-4 h-4 mr-1" /> History
              </TabsTrigger>
            </TabsList>

            <TabsContent value="chat" className="space-y-6">
              <AgentChat agentChat={agentChat} />
            </TabsContent>

            <TabsContent value="agents" className="space-y-6">
              <AgentPanels sessionData={sessionData} />
            </TabsContent>

            <TabsContent value="history" className="space-y-6">
              <SessionHistory actionLogs={agentChat.actionLogs} />
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </ErrorBoundary>
  );
};

export default Index;
