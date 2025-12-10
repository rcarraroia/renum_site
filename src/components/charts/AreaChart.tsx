import React from 'react';
import { ResponsiveContainer, AreaChart as RechartsAreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { MetricData } from '@/types/sicc';
import { cn } from '@/lib/utils';

interface AreaChartProps {
    data: MetricData[];
    dataKey: string;
    areaColor: string;
    title: string;
    unit?: string;
    className?: string;
}

const AreaChart: React.FC<AreaChartProps> = ({ data, dataKey, areaColor, title, unit = '', className }) => {
    return (
        <div className={cn("h-[300px] w-full", className)}>
            <ResponsiveContainer width="100%" height="100%">
                <RechartsAreaChart data={data} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis dataKey="date" stroke="hsl(var(--foreground))" tickFormatter={(tick) => tick.substring(5)} />
                    <YAxis stroke="hsl(var(--foreground))" domain={[80, 100]} />
                    <Tooltip 
                        contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '0.5rem' }}
                        labelStyle={{ color: 'hsl(var(--primary))' }}
                        formatter={(value, name) => [`${value}${unit}`, name]}
                    />
                    <Area 
                        type="monotone" 
                        dataKey={dataKey} 
                        stroke={areaColor} 
                        fill={areaColor} 
                        fillOpacity={0.3}
                        name={title}
                    />
                </RechartsAreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default AreaChart;