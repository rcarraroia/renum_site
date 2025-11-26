import React, { useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { cn } from '@/lib/utils';

interface ChartData {
    name: string;
    [key: string]: any;
}

interface ReportChartProps {
    title: string;
    description?: string;
    data: ChartData[];
    type: 'bar' | 'line' | 'pie' | 'donut';
    dataKeys: { key: string; color: string; name: string; type?: 'line' | 'bar' }[];
    className?: string;
}

const COLORS = ['#4e4ea8', '#FF6B35', '#0ca7d2', '#10b981', '#f59e0b', '#ef4444'];

const ReportChart: React.FC<ReportChartProps> = ({ title, description, data, type, dataKeys, className }) => {
    const ChartComponent = useMemo(() => {
        switch (type) {
            case 'bar':
                return (
                    <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" stroke="hsl(var(--foreground))" />
                        <YAxis stroke="hsl(var(--foreground))" />
                        <Tooltip 
                            contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '0.5rem' }}
                            labelStyle={{ color: 'hsl(var(--primary))' }}
                        />
                        <Legend />
                        {dataKeys.map((item, index) => (
                            <Bar key={item.key} dataKey={item.key} fill={item.color} name={item.name} radius={[4, 4, 0, 0]} />
                        ))}
                    </BarChart>
                );
            case 'line':
                return (
                    <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" stroke="hsl(var(--foreground))" />
                        <YAxis stroke="hsl(var(--foreground))" />
                        <Tooltip 
                            contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '0.5rem' }}
                            labelStyle={{ color: 'hsl(var(--primary))' }}
                        />
                        <Legend />
                        {dataKeys.map((item, index) => (
                            <Line 
                                key={item.key} 
                                type="monotone" 
                                dataKey={item.key} 
                                stroke={item.color} 
                                name={item.name} 
                                strokeWidth={2}
                                dot={{ r: 4 }}
                                activeDot={{ r: 8 }}
                            />
                        ))}
                    </LineChart>
                );
            case 'pie':
            case 'donut':
                return (
                    <PieChart>
                        <Pie
                            data={data}
                            dataKey="value"
                            nameKey="name"
                            cx="50%"
                            cy="50%"
                            outerRadius={type === 'donut' ? 120 : 150}
                            innerRadius={type === 'donut' ? 80 : 0}
                            fill="#8884d8"
                            paddingAngle={5}
                            labelLine={false}
                            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.fill || COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip 
                            contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '0.5rem' }}
                            labelStyle={{ color: 'hsl(var(--primary))' }}
                        />
                        <Legend layout="vertical" align="right" verticalAlign="middle" />
                    </PieChart>
                );
            default:
                return <div className="text-center text-red-500">Tipo de gráfico não suportado.</div>;
        }
    }, [data, type, dataKeys]);

    return (
        <Card className={cn("h-full", className)}>
            <CardHeader>
                <CardTitle>{title}</CardTitle>
                {description && <p className="text-sm text-muted-foreground">{description}</p>}
            </CardHeader>
            <CardContent className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    {ChartComponent}
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
};

export default ReportChart;