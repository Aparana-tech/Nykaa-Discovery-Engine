import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div style={{ background: 'rgba(15, 17, 23, 0.95)', border: '1px solid var(--border-color)', padding: '16px', borderRadius: '12px', backdropFilter: 'blur(10px)', color: 'white' }}>
        <p style={{ fontWeight: 'bold', marginBottom: '8px', textTransform: 'capitalize', color: 'var(--accent-secondary)' }}>{data.friction_point}</p>
        <p style={{ fontSize: '0.9rem', marginBottom: '4px' }}>Impact Score: <span style={{fontWeight: '600'}}>{data.impact_score.toFixed(3)}</span></p>
        <p style={{ fontSize: '0.9rem' }}>Mentions: <span style={{fontWeight: '600'}}>{data.volume_count}</span></p>
      </div>
    );
  }
  return null;
};

const PrioritizationMatrix = ({ data }) => {
  
  // Sort by impact score and take top 15 so the line chart is clean and readable
  const sortedData = [...data]
    .sort((a, b) => (b.composite_score || 0) - (a.composite_score || 0))
    .slice(0, 15);

  const chartData = sortedData.map((item, index) => ({
    name: `Issue #${index + 1}`,
    friction_point: item.friction_point,
    impact_score: item.composite_score || 0,
    volume_count: item.evidence.review_count || 0
  }));

  return (
    <div style={{ width: '100%', height: 280, marginTop: '20px' }}>
      <ResponsiveContainer>
        <LineChart margin={{ top: 20, right: 30, bottom: 20, left: 10 }} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
          
          <XAxis 
            dataKey="name" 
            stroke="var(--text-muted)"
            tick={{fill: 'var(--text-muted)', fontSize: 12}}
          />
          
          <YAxis 
            dataKey="impact_score"
            name="Impact Score" 
            stroke="var(--text-muted)"
            domain={[0, 'auto']}
            tick={{fill: 'var(--text-muted)'}}
            label={{ value: 'Impact Score', angle: -90, position: 'insideLeft', fill: 'var(--text-muted)' }}
          />
          
          <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3', stroke: 'rgba(255,255,255,0.2)' }} />
          
          <Line 
            type="monotone" 
            dataKey="impact_score" 
            stroke="var(--accent-primary)" 
            strokeWidth={3}
            dot={{ fill: 'var(--accent-secondary)', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, fill: 'var(--accent-primary)' }}
          />
        </LineChart>
      </ResponsiveContainer>
      <div style={{textAlign: 'center', marginTop: '16px', fontSize: '0.85rem', color: 'var(--text-muted)'}}>
         Showing the top 15 friction points by overall Impact Score.
      </div>
    </div>
  );
};

export default PrioritizationMatrix;
