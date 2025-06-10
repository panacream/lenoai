
import React, { useState, useRef } from 'react';
import { useAgentChat } from '@/hooks/useAgentChat';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Code, 
  Coins, 
  Users, 
  Mail, 
  Globe, 
  Send,
  Upload,
  Download,
  Settings
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface AgentPanelsProps {
  sessionData: any;
}

export const AgentPanels: React.FC<AgentPanelsProps> = ({ sessionData }) => {
  const [activePanel, setActivePanel] = useState('coding');
  const { toast } = useToast();
  const { sendMessage } = useAgentChat();

  // Refs for all relevant input fields
  // Coding
  const repoUrlRef = useRef<HTMLInputElement>(null);
  const branchRef = useRef<HTMLInputElement>(null);
  const codePromptRef = useRef<HTMLTextAreaElement>(null);
  const codeLangRef = useRef<{ value?: string }>({});
  // Token
  const walletAddressRef = useRef<HTMLInputElement>(null);
  const recipientRef = useRef<HTMLInputElement>(null);
  const amountRef = useRef<HTMLInputElement>(null);
  // Social
  const postContentRef = useRef<HTMLTextAreaElement>(null);
  const postVisibilityRef = useRef<{ value?: string }>({});
  const profileUpdateRef = useRef<HTMLTextAreaElement>(null);
  // Google (Gmail)
  const emailToRef = useRef<HTMLInputElement>(null);
  const emailSubjectRef = useRef<HTMLInputElement>(null);
  const emailBodyRef = useRef<HTMLTextAreaElement>(null);
  // Sheets
  const sheetUrlRef = useRef<HTMLInputElement>(null);
  // Scraper
  const scrapeUrlRef = useRef<HTMLInputElement>(null);
  const selectorsRef = useRef<HTMLInputElement>(null);
  const dataFormatRef = useRef<{ value?: string }>({});
  const analysisTypeRef = useRef<{ value?: string }>({});
  const analysisPromptRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = async (agentType: string, action: string) => {
    let message = '';
    try {
      switch (agentType) {
        case 'Coding':
          if (action === 'clone repository') {
            const url = repoUrlRef.current?.value || '';
            const branch = branchRef.current?.value || '';
            message = `Clone the repository at ${url}${branch ? ' on branch ' + branch : ''}.`;
          } else if (action === 'analyze repository') {
            const url = repoUrlRef.current?.value || '';
            message = `Analyze the repository at ${url}.`;
          } else if (action === 'generate code') {
            const prompt = codePromptRef.current?.value || '';
            const lang = codeLangRef.current.value || '';
            message = `Generate ${lang} code: ${prompt}`;
          }
          break;
        case 'Token':
          if (action === 'check balance') {
            const addr = walletAddressRef.current?.value || '';
            message = `Check token balance for address ${addr}.`;
          } else if (action === 'get metadata') {
            const addr = walletAddressRef.current?.value || '';
            message = `Get token metadata for address ${addr}.`;
          } else if (action === 'transfer tokens') {
            const to = recipientRef.current?.value || '';
            const amt = amountRef.current?.value || '';
            message = `Transfer ${amt} LENOAI tokens to ${to}.`;
          }
          break;
        case 'Social':
          if (action === 'create LinkedIn post') {
            const content = postContentRef.current?.value || '';
            const vis = postVisibilityRef.current.value || '';
            message = `Post to LinkedIn: "${content}" Visibility: ${vis}.`;
          } else if (action === 'update profile') {
            const update = profileUpdateRef.current?.value || '';
            message = `Update LinkedIn profile: ${update}`;
          }
          break;
        case 'Google':
          if (action === 'send email') {
            const to = emailToRef.current?.value || '';
            const subject = emailSubjectRef.current?.value || '';
            const body = emailBodyRef.current?.value || '';
            message = `Send an email to ${to} with subject "${subject}" and body "${body}".`;
          } else if (action === 'read sheet') {
            const url = sheetUrlRef.current?.value || '';
            message = `Read Google Sheet at ${url}.`;
          } else if (action === 'update sheet') {
            const url = sheetUrlRef.current?.value || '';
            message = `Update Google Sheet at ${url}.`;
          } else if (action === 'calendar event') {
            message = `Create a new Google Calendar event.`;
          }
          break;
        case 'Scraper':
          if (action === 'scrape website') {
            const url = scrapeUrlRef.current?.value || '';
            const selectors = selectorsRef.current?.value || '';
            const format = dataFormatRef.current.value || '';
            message = `Scrape website ${url}${selectors ? ' with selectors ' + selectors : ''}${format ? ' and output as ' + format : ''}.`;
          } else if (action === 'analyze data') {
            const type = analysisTypeRef.current.value || '';
            const prompt = analysisPromptRef.current?.value || '';
            message = `Analyze scraped data (${type}): ${prompt}`;
          }
          break;
        default:
          message = `${agentType} agent: ${action}`;
      }
      if (!message.trim()) {
        toast({ title: 'Missing input', description: 'Please fill out required fields.', variant: 'destructive' });
        return;
      }
      await sendMessage(message);
      toast({ title: `${agentType} Agent`, description: `Action sent: ${action}`, variant: 'success' });
    } catch (err) {
      toast({ title: `${agentType} Agent`, description: `Error: ${err instanceof Error ? err.message : String(err)}`, variant: 'destructive' });
    }
  };


  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Agent Control Panels</h2>
        <p className="text-slate-600">Direct interaction with specialized agents</p>
      </div>

      <Tabs value={activePanel} onValueChange={setActivePanel}>
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="coding" className="flex items-center space-x-2">
            <Code className="w-4 h-4" />
            <span className="hidden sm:inline">Coding</span>
          </TabsTrigger>
          <TabsTrigger value="token" className="flex items-center space-x-2">
            <Coins className="w-4 h-4" />
            <span className="hidden sm:inline">Token</span>
          </TabsTrigger>
          <TabsTrigger value="social" className="flex items-center space-x-2">
            <Users className="w-4 h-4" />
            <span className="hidden sm:inline">Social</span>
          </TabsTrigger>
          <TabsTrigger value="google" className="flex items-center space-x-2">
            <Mail className="w-4 h-4" />
            <span className="hidden sm:inline">Google</span>
          </TabsTrigger>
          <TabsTrigger value="scraper" className="flex items-center space-x-2">
            <Globe className="w-4 h-4" />
            <span className="hidden sm:inline">Scraper</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="coding" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Code className="w-5 h-5" />
                  <span>Repository Operations</span>
                </CardTitle>
                <CardDescription>Manage GitHub repositories and files</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="repo-url">Repository URL</Label>
                  <Input 
                    id="repo-url" 
                    placeholder="https://github.com/user/repo"
                    className="mt-1"
                    ref={repoUrlRef}
                  />
                </div>
                <div>
                  <Label htmlFor="branch">Branch</Label>
                  <Input 
                    id="branch" 
                    placeholder="main"
                    className="mt-1"
                    ref={branchRef}
                  />
                </div>
                <div className="flex space-x-2">
                  <Button 
                    className="flex-1"
                    onClick={() => handleSubmit('Coding', 'clone repository')}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Clone
                  </Button>
                  <Button 
                    variant="outline" 
                    className="flex-1"
                    onClick={() => handleSubmit('Coding', 'analyze repository')}
                  >
                    <Settings className="w-4 h-4 mr-2" />
                    Analyze
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Code Generation</CardTitle>
                <CardDescription>Generate and refactor code</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="code-prompt">Code Request</Label>
                  <Textarea 
                    id="code-prompt" 
                    placeholder="Describe the code you want to generate..."
                    className="mt-1"
                    rows={3}
                    ref={codePromptRef}
                  />
                </div>
                <div>
                  <Label htmlFor="language">Language</Label>
                  <Select
                    onValueChange={val => (codeLangRef.current.value = val)}
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select language" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="javascript">JavaScript</SelectItem>
                      <SelectItem value="python">Python</SelectItem>
                      <SelectItem value="typescript">TypeScript</SelectItem>
                      <SelectItem value="react">React</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button 
                  className="w-full bg-green-500 hover:bg-green-600"
                  onClick={() => handleSubmit('Coding', 'generate code')}
                >
                  <Code className="w-4 h-4 mr-2" />
                  Generate Code
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="token" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Coins className="w-5 h-5" />
                  <span>Wallet Operations</span>
                </CardTitle>
                <CardDescription>LENOAI token management</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="wallet-address">Wallet Address</Label>
                  <Input 
                    id="wallet-address" 
                    placeholder="0x..."
                    className="mt-1"
                    ref={walletAddressRef}
                  />
                </div>
                <div className="flex space-x-2">
                  <Button 
                    variant="outline" 
                    className="flex-1"
                    onClick={() => handleSubmit('Token', 'check balance')}
                  >
                    Check Balance
                  </Button>
                  <Button 
                    variant="outline" 
                    className="flex-1"
                    onClick={() => handleSubmit('Token', 'get metadata')}
                  >
                    Metadata
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Token Transfer</CardTitle>
                <CardDescription>Send LENOAI tokens</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="recipient">Recipient Address</Label>
                  <Input 
                    id="recipient" 
                    placeholder="0x..."
                    className="mt-1"
                    ref={recipientRef}
                  />
                </div>
                <div>
                  <Label htmlFor="amount">Amount</Label>
                  <Input 
                    id="amount" 
                    type="number" 
                    placeholder="0.00"
                    className="mt-1"
                    ref={amountRef}
                  />
                </div>
                <Button 
                  className="w-full bg-yellow-500 hover:bg-yellow-600"
                  onClick={() => handleSubmit('Token', 'transfer tokens')}
                >
                  <Send className="w-4 h-4 mr-2" />
                  Transfer Tokens
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="social" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Users className="w-5 h-5" />
                  <span>LinkedIn Operations</span>
                </CardTitle>
                <CardDescription>Manage LinkedIn profile and posts</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="post-content">Post Content</Label>
                  <Textarea 
                    id="post-content" 
                    placeholder="What's on your mind?"
                    className="mt-1"
                    rows={3}
                    ref={postContentRef}
                  />
                </div>
                <div>
                  <Label htmlFor="post-visibility">Visibility</Label>
                  <Select
                    onValueChange={val => (postVisibilityRef.current.value = val)}
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select visibility" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="public">Public</SelectItem>
                      <SelectItem value="connections">Connections Only</SelectItem>
                      <SelectItem value="private">Private</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button 
                  className="w-full bg-purple-500 hover:bg-purple-600"
                  onClick={() => handleSubmit('Social', 'create LinkedIn post')}
                >
                  <Send className="w-4 h-4 mr-2" />
                  Post to LinkedIn
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Profile Management</CardTitle>
                <CardDescription>Update social media profiles</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Available Platforms</Label>
                  <div className="flex flex-wrap gap-2 mt-2">
                    <Badge>LinkedIn</Badge>
                    <Badge variant="outline">Meta (Coming Soon)</Badge>
                    <Badge variant="outline">Twitter (Coming Soon)</Badge>
                    <Badge variant="outline">TikTok (Coming Soon)</Badge>
                  </div>
                </div>
                <div>
                  <Label htmlFor="profile-update">Profile Update</Label>
                  <Textarea 
                    id="profile-update" 
                    placeholder="Describe profile changes..."
                    className="mt-1"
                    rows={2}
                    ref={profileUpdateRef}
                  />
                </div>
                <Button 
                  variant="outline" 
                  className="w-full"
                  onClick={() => handleSubmit('Social', 'update profile')}
                >
                  <Settings className="w-4 h-4 mr-2" />
                  Update Profile
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="google" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Mail className="w-5 h-5" />
                  <span>Gmail Operations</span>
                </CardTitle>
                <CardDescription>Email management and automation</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="email-to">To</Label>
                  <Input 
                    id="email-to" 
                    placeholder="recipient@example.com"
                    className="mt-1"
                    ref={emailToRef}
                  />
                </div>
                <div>
                  <Label htmlFor="email-subject">Subject</Label>
                  <Input 
                    id="email-subject" 
                    placeholder="Email subject"
                    className="mt-1"
                    ref={emailSubjectRef}
                  />
                </div>
                <div>
                  <Label htmlFor="email-body">Message</Label>
                  <Textarea 
                    id="email-body" 
                    placeholder="Email content..."
                    className="mt-1"
                    rows={3}
                    ref={emailBodyRef}
                  />
                </div>
                <Button 
                  className="w-full bg-red-500 hover:bg-red-600"
                  onClick={() => handleSubmit('Google', 'send email')}
                >
                  <Send className="w-4 h-4 mr-2" />
                  Send Email
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Sheets & Calendar</CardTitle>
                <CardDescription>Spreadsheet and calendar operations</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="sheet-url">Google Sheet URL</Label>
                  <Input 
                    id="sheet-url" 
                    placeholder="https://docs.google.com/spreadsheets/..."
                    className="mt-1"
                    ref={sheetUrlRef}
                  />
                </div>
                <div className="flex space-x-2">
                  <Button 
                    variant="outline" 
                    className="flex-1"
                    onClick={() => handleSubmit('Google', 'read sheet')}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Read
                  </Button>
                  <Button 
                    variant="outline" 
                    className="flex-1"
                    onClick={() => handleSubmit('Google', 'update sheet')}
                  >
                    <Upload className="w-4 h-4 mr-2" />
                    Update
                  </Button>
                </div>
                <Button 
                  className="w-full"
                  onClick={() => handleSubmit('Google', 'calendar event')}
                >
                  <Settings className="w-4 h-4 mr-2" />
                  Create Calendar Event
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="scraper" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Globe className="w-5 h-5" />
                  <span>Web Scraping</span>
                </CardTitle>
                <CardDescription>Extract data from websites</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="scrape-url">Target URL</Label>
                  <Input 
                    id="scrape-url" 
                    placeholder="https://example.com"
                    className="mt-1"
                    ref={scrapeUrlRef}
                  />
                </div>
                <div>
                  <Label htmlFor="selectors">CSS Selectors (optional)</Label>
                  <Input 
                    id="selectors" 
                    placeholder=".content, h1, .price"
                    className="mt-1"
                    ref={selectorsRef}
                  />
                </div>
                <div>
                  <Label htmlFor="data-format">Output Format</Label>
                  <Select
                    onValueChange={val => (dataFormatRef.current.value = val)}
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select format" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="json">JSON</SelectItem>
                      <SelectItem value="csv">CSV</SelectItem>
                      <SelectItem value="xml">XML</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button 
                  className="w-full bg-indigo-500 hover:bg-indigo-600"
                  onClick={() => handleSubmit('Scraper', 'scrape website')}
                >
                  <Globe className="w-4 h-4 mr-2" />
                  Start Scraping
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Data Analysis</CardTitle>
                <CardDescription>Process extracted data</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="analysis-type">Analysis Type</Label>
                  <Select
                    onValueChange={val => (analysisTypeRef.current.value = val)}
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select analysis" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="content">Content Analysis</SelectItem>
                      <SelectItem value="sentiment">Sentiment Analysis</SelectItem>
                      <SelectItem value="keyword">Keyword Extraction</SelectItem>
                      <SelectItem value="structure">Structure Analysis</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="analysis-prompt">Analysis Instructions</Label>
                  <Textarea 
                    id="analysis-prompt" 
                    placeholder="What insights are you looking for?"
                    className="mt-1"
                    rows={3}
                    ref={analysisPromptRef}
                  />
                </div>
                <Button 
                  variant="outline" 
                  className="w-full"
                  onClick={() => handleSubmit('Scraper', 'analyze data')}
                >
                  <Settings className="w-4 h-4 mr-2" />
                  Analyze Data
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};
