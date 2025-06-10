
import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  History, 
  Search, 
  Filter, 
  Download, 
  Trash2,
  Clock,
  CheckCircle,
  XCircle,
  Code,
  Coins,
  Users,
  Mail,
  Globe,
  Bot
} from 'lucide-react';



const agentIcons = {
  coding: Code,
  token: Coins,
  social: Users,
  google: Mail,
  scraper: Globe,
  manager: Bot,
  'Leno AI': Bot
};

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed':
      return 'text-green-600 bg-green-100';
    case 'failed':
      return 'text-red-600 bg-red-100';
    case 'processing':
      return 'text-blue-600 bg-blue-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'completed':
      return <CheckCircle className="w-4 h-4" />;
    case 'failed':
      return <XCircle className="w-4 h-4" />;
    case 'processing':
      return <Clock className="w-4 h-4" />;
    default:
      return <Clock className="w-4 h-4" />;
  }
};

type TaskHistoryItem = {
  user: string;
  request: string;
  response: string;
  timestamp: string;
  status: string;
};

export const SessionHistory: React.FC = () => {
  const [history, setHistory] = useState<TaskHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    async function fetchHistory() {
      setLoading(true);
      try {
        const res = await fetch('/api/task_history');
        if (!res.ok) throw new Error('Failed to fetch task history');
        const data = await res.json();
        setHistory(Array.isArray(data) ? data.reverse() : []);
        setError(null);
      } catch (err: unknown) {
        if (typeof err === 'object' && err !== null && 'message' in err) {
          setError((err as { message?: string }).message || 'Unknown error');
        } else {
          setError('Unknown error');
        }
      }
      setLoading(false);
    }
    fetchHistory();
  }, []);

  const filteredHistory = history.filter(item => {
    const matchesSearch = item.request.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.response.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || item.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const exportHistory = () => {
    const data = filteredHistory.map(item => ({
      Request: item.request,
      Response: item.response,
      Status: item.status,
      Timestamp: item.timestamp
    }));

    if (data.length === 0) return;
    const csv = [
      Object.keys(data[0]).join(','),
      ...data.map(row => Object.values(row).map(value => `"${value}"`).join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'agent-history.csv';
    a.click();
  };


  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Session History</h2>
        <p className="text-slate-600">Track all agent activities and task outcomes</p>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <History className="w-5 h-5" />
            <span>Task History</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search tasks and outputs..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Status</option>
                <option value="completed">Completed</option>
                <option value="processing">Processing</option>
                <option value="failed">Failed</option>
              </select>
              <Button onClick={exportHistory} variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* History List */}
      <Card>
        <CardContent className="p-0">
          <ScrollArea className="h-[500px]">
            <div className="divide-y divide-gray-200">
              {filteredHistory.map((item, idx) => (
                <div key={idx} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4 flex-1">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Bot className="w-5 h-5 text-blue-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="text-sm font-medium text-gray-900 truncate">
                            {item.request}
                          </h3>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{item.response}</p>
                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                          <span>{new Date(item.timestamp).toLocaleDateString()} at {new Date(item.timestamp).toLocaleTimeString()}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      <Badge className={`${getStatusColor(item.status)} border-0`}>
                        <div className="flex items-center space-x-1">
                          {getStatusIcon(item.status)}
                          <span className="capitalize">{item.status}</span>
                        </div>
                      </Badge>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {filteredHistory.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <History className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No history found</h3>
            <p className="text-gray-600">
              {searchTerm || filterStatus !== 'all'
                ? 'Try adjusting your filters or search terms.'
                : 'Start using the agents to see your activity history here.'}
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
