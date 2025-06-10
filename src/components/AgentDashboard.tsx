
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Code, 
  Globe, 
  Coins, 
  Users, 
  Mail, 
  Activity,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react';

const agentData = [
  {
    id: 'manager',
    name: 'Manager Agent',
    description: 'Root orchestrator for all agent operations',
    icon: Activity,
    status: 'active',
    color: 'bg-blue-500',
    capabilities: ['Task Routing', 'Workflow Orchestration', 'Session Management'],
    lastActive: '2 minutes ago'
  },
  {
    id: 'coding',
    name: 'Coding Agent',
    description: 'GitHub operations, code generation, debugging',
    icon: Code,
    status: 'active',
    color: 'bg-green-500',
    capabilities: ['GitHub Integration', 'Code Generation', 'Repository Management'],
    lastActive: '5 minutes ago'
  },
  {
    id: 'token',
    name: 'Token Agent',
    description: 'LENOAI token and wallet operations',
    icon: Coins,
    status: 'active',
    color: 'bg-yellow-500',
    capabilities: ['Balance Checks', 'Token Transfers', 'Minting/Burning'],
    lastActive: '1 hour ago'
  },
  {
    id: 'social',
    name: 'Social Media Agent',
    description: 'LinkedIn, Meta, Twitter, TikTok operations',
    icon: Users,
    status: 'idle',
    color: 'bg-purple-500',
    capabilities: ['LinkedIn Posts', 'Profile Management', 'Event Handling'],
    lastActive: '3 hours ago'
  },
  {
    id: 'google',
    name: 'Google Agent',
    description: 'Gmail, Sheets, Calendar integration',
    icon: Mail,
    status: 'active',
    color: 'bg-red-500',
    capabilities: ['Email Management', 'Spreadsheet Operations', 'Calendar Events'],
    lastActive: '30 minutes ago'
  },
  {
    id: 'scraper',
    name: 'Scraper Agent',
    description: 'Advanced web scraping and data extraction',
    icon: Globe,
    status: 'idle',
    color: 'bg-indigo-500',
    capabilities: ['Web Scraping', 'Data Extraction', 'Content Analysis'],
    lastActive: '2 hours ago'
  }
];

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'active':
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    case 'idle':
      return <Clock className="w-4 h-4 text-yellow-500" />;
    case 'error':
      return <AlertCircle className="w-4 h-4 text-red-500" />;
    default:
      return <Clock className="w-4 h-4 text-gray-500" />;
  }
};

interface AgentDashboardProps {
  sessionData: any;
}

export const AgentDashboard: React.FC<AgentDashboardProps> = ({ sessionData }) => {
  const activeAgents = agentData.filter(agent => agent.status === 'active').length;
  const systemHealth = Math.round((activeAgents / agentData.length) * 100);

  return (
    <div className="space-y-6">
      {/* System Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeAgents}/{agentData.length}</div>
            <p className="text-xs text-muted-foreground">
              {activeAgents} agents currently active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">System Health</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{systemHealth}%</div>
            <Progress value={systemHealth} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Session Status</CardTitle>
            <Globe className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {sessionData.isConnected ? 'Online' : 'Offline'}
            </div>
            <p className="text-xs text-muted-foreground">
              Backend connectivity status
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Agent Grid */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 mb-4">Available Agents</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agentData.map((agent) => {
            const IconComponent = agent.icon;
            return (
              <Card key={agent.id} className="hover:shadow-lg transition-shadow duration-200">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 ${agent.color} rounded-lg flex items-center justify-center`}>
                        <IconComponent className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">{agent.name}</CardTitle>
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(agent.status)}
                          <Badge variant={agent.status === 'active' ? 'default' : 'secondary'}>
                            {agent.status}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  </div>
                  <CardDescription>{agent.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-slate-900 mb-2">Capabilities</h4>
                    <div className="flex flex-wrap gap-2">
                      {agent.capabilities.map((capability, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {capability}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div className="flex justify-between items-center text-sm text-slate-600">
                    <span>Last active: {agent.lastActive}</span>
                    <Button size="sm" variant="outline">
                      Configure
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
};
