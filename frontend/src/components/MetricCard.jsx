import React from 'react';

const MetricCard = ({ title, value, subtitle, icon, delayClass }) => {
  return (
    <div className={`glass-card animate-fade-in ${delayClass}`} style={{display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px'}}>
        <h3 style={{fontSize: '1.05rem', margin: 0}}>{title}</h3>
        <div style={{padding: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '12px'}}>
          {icon}
        </div>
      </div>
      <div>
        <div style={{fontSize: 'clamp(1.4rem, 2.5vw, 2.2rem)', fontWeight: '700', color: 'var(--text-main)', marginBottom: '4px', wordBreak: 'break-word', letterSpacing: '-0.5px'}}>
          {value}
        </div>
        <div style={{fontSize: '0.9rem', color: 'var(--text-muted)'}}>
          {subtitle}
        </div>
      </div>
    </div>
  );
};

export default MetricCard;
