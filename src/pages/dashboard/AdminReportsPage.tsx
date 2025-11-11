import React, { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, FileText, Calendar, Download, Printer, Settings, Wrench, Users, Clock, List, BarChart } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { DateRange } from 'react-day-picker';
import { Calendar as CalendarIcon } from 'lucide-react';
import { Calendar as CalendarComponent } from '@/components/ui/calendar';

// Import Tab Components
import ReportsOverviewTab from '@/components/reports/ReportsOverviewTab';
import RenusPerformanceTab from '@/components/reports/RenusPerformanceTab';
import ClientProjectReportsTab from '@/components/reports/ClientProjectReportsTab';
import CustomReportBuilderTab from '@/components/reports/CustomReportBuilderTab';
import SavedReportsTab from '@/components/reports/SavedReportsTab';

const AdminReportsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [dateRange, setDateRange] = useState<DateRange | undefined>({
    from: new Date(new Date().setDate(new Date().getDate() - 30)),
    to: new Date(),
  });

  const tabs = [
    { value: 'overview', label: 'Visão Geral', icon: BarChart, component: ReportsOverviewTab },
    { value: 'renus', label: 'Performance Renus', icon: Zap, component: RenusPerformanceTab },
    { value: 'projects', label: 'Clientes & Projetos', icon: Users, component: ClientProjectReportsTab },
    { value: 'custom', label: 'Construtor', icon: Wrench, component: CustomReportBuilderTab },
    { value: 'saved', label: 'Salvos', icon: List, component: SavedReportsTab },
  ];

  const handleExport = (format: string) => {
    toast.info(`Exportando relatório (${activeTab}) para ${format}...`);
    // Mock export logic
    setTimeout(() => {
        toast.success(`Exportação para ${format} concluída!`);
    }, 1000);
  };

  const handlePrint = () => {
    toast.info("Preparando para impressão...");
    window.print();
  };

  const handleDateRangeSelect = (range: string) => {
    const today = new Date();
    let fromDate: Date;
    let toDate: Date = today;

    switch (range) {
        case '7days':
            fromDate = new Date(today.setDate(today.getDate() - 7));
            break;
        case '30days':
            fromDate = new Date(today.setDate(today.getDate() - 30));
            break;
        case 'month':
            fromDate = new Date(today.getFullYear(), today.getMonth(), 1);
            break;
        default:
            return; // Use current custom range
    }
    setDateRange({ from: fromDate, to: toDate });
  };

  const dateRangeDisplay = dateRange?.from 
    ? `${format(dateRange.from, 'dd/MM/yyyy', { locale: ptBR })} - ${dateRange.to ? format(dateRange.to, 'dd/MM/yyyy', { locale: ptBR }) : 'Hoje'}`
    : 'Selecione o Período';

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <FileText className="h-7 w-7 mr-3 text-[#0ca7d2]" />
          Relatórios
        </h2>
        <div className="flex space-x-2">
            <Button variant="outline" onClick={handlePrint}>
                <Printer className="h-4 w-4 mr-2" /> Imprimir
            </Button>
            <Select onValueChange={handleExport}>
                <SelectTrigger className="w-[120px]">
                    <Download className="h-4 w-4 mr-2" />
                    <SelectValue placeholder="Exportar" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="PDF">PDF</SelectItem>
                    <SelectItem value="Excel">Excel</SelectItem>
                    <SelectItem value="CSV">CSV</SelectItem>
                </SelectContent>
            </Select>
        </div>
      </div>

      {/* Date Range and Filters */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 p-4 bg-card rounded-lg shadow-sm border">
        <div className="flex items-center space-x-4 mb-4 md:mb-0">
            <Clock className="h-5 w-5 text-muted-foreground" />
            <span className="font-semibold text-sm">Período:</span>
            
            <Select defaultValue="30days" onValueChange={handleDateRangeSelect}>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Últimos 30 dias" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="7days">Últimos 7 dias</SelectItem>
                    <SelectItem value="30days">Últimos 30 dias</SelectItem>
                    <SelectItem value="month">Este Mês</SelectItem>
                    <SelectItem value="custom">Período Personalizado</SelectItem>
                </SelectContent>
            </Select>
        </div>

        <Popover>
            <PopoverTrigger asChild>
                <Button
                    id="date"
                    variant={"outline"}
                    className={cn(
                        "w-[300px] justify-start text-left font-normal",
                        !dateRange && "text-muted-foreground"
                    )}
                >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {dateRangeDisplay}
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0" align="end">
                <CalendarComponent
                    initialFocus
                    mode="range"
                    defaultMonth={dateRange?.from}
                    selected={dateRange}
                    onSelect={setDateRange}
                    numberOfMonths={2}
                />
            </PopoverContent>
        </Popover>
      </div>

      {/* Main Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5 h-auto p-1 bg-gray-100 dark:bg-gray-800">
          {tabs.map(tab => (
            <TabsTrigger 
              key={tab.value} 
              value={tab.value} 
              className={cn(
                "flex items-center space-x-2 data-[state=active]:bg-[#FF6B35] data-[state=active]:text-white data-[state=active]:shadow-md transition-all",
                activeTab === tab.value && 'bg-[#FF6B35] text-white'
              )}
            >
              <tab.icon className="h-4 w-4" />
              <span className="hidden sm:inline">{tab.label}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {tabs.map(tab => (
          <TabsContent key={tab.value} value={tab.value} className="mt-6">
            <tab.component />
          </TabsContent>
        ))}
      </Tabs>
    </DashboardLayout>
  );
};

export default AdminReportsPage;