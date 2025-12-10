import React from 'react';
import { ResponsiveContainer, LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { MetricData } from '@/types/sicc';
import { cn } from '@/lib/utils';

interface LineChartProps {
    data: MetricData[];
    dataKey: string;
    lineColor: string;
    title: string;
    className?: string;
}

const LineChart: React.FC<LineChartProps> = ({ data, dataKey, lineColor, title, className }) => {
    return (
        <div className={cn("h-[300px] w-full", className)}>
            <ResponsiveContainer width="100%" height="100%">
                <RechartsLineChart data={data} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis dataKey="date" stroke="hsl(var(--foreground))" tickFormatter={(tick) => tick.substring(5)} />
                    <YAxis stroke="hsl(var(--foreground))" />
                    <Tooltip 
                        contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '0.5rem' }}
                        labelStyle={{ color: 'hsl(var(--primary))' }}
                        formatter={(value, name) => [`${value} ${title}`, name]}
                    />
                    <Line 
                        type="monotone" 
                        dataKey={dataKey} 
                        stroke={lineColor} 
                        strokeWidth={2}
                        dot={{ r: 4 }}
                        activeDot={{ r: 8 }}
                        name={title}
                    />
                </RechartsLineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default LineChart;