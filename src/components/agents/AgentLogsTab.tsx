import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Terminal, Clock } from 'lucide-react';
import { Textarea } from '@/components/ui/textarea';

const MOCK_LOGS = `[2025-01-20 14:30:01] INFO: Conversation conv-123 started via WhatsApp.
[2025-01-20 14:30:05] DEBUG: PII Detector ran on user input. Result: Sanitized.
[2025-01-20 14:30:10] TOOL_CALL: Calling schedule_call tool with params { email: 'joao@slim.com' }
[2025-01-20 14:30:12] SUCCESS: Tool schedule_call returned 200 OK.
[2025-01-20 14:30:15] INFO: Renus response sent. Latency: 1.2s.`;

const AgentLogsTab: React.FC = () => {
  return (
    <Card>
      <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Terminal className="h-5 w-5 mr-2" /> Logs de Execução</CardTitle></CardHeader>
      <CardContent>
        <Textarea 
          readOnly 
          rows={15} 
          defaultValue={MOCK_LOGS} 
          className="font-mono text-xs bg-gray-900 text-green-400 resize-none"
        />
      </CardContent>
    </Card>
  );
};

export default AgentLogsTab;