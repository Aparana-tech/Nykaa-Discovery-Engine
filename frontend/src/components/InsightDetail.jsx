import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Quote, AlertCircle, CheckCircle2 } from 'lucide-react';

const InsightDetail = ({ insight }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Parse data
  const title = insight.friction_point;
  const score = insight.composite_score ? insight.composite_score.toFixed(3) : "0.000";
  const revenueAtRisk = insight.business_impact.estimated_monthly_revenue_at_risk;
  const quotes = insight.evidence.sample_quotes;
  const severity = insight.priority ? insight.priority.split(' ')[1] : 'Unknown';
  
  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

  return (
    <div style={{ border: '1px solid var(--border-color)', borderRadius: '12px', overflow: 'hidden', background: 'rgba(255,255,255,0.02)'}}>
      {/* Header (Clickable) */}
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        style={{ padding: '16px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer', background: isExpanded ? 'rgba(255,255,255,0.05)' : 'transparent', transition: 'background 0.2s' }}
      >
        <div>
          <h3 style={{ textTransform: 'capitalize', color: 'var(--text-main)', marginBottom: '4px', fontSize: '1.1rem' }}>
            {title}
          </h3>
          <div style={{ display: 'flex', gap: '12px', fontSize: '0.85rem', color: 'var(--text-muted)', alignItems: 'center' }}>
            <span>Score: <strong style={{color: 'white'}}>{score}</strong></span>
            <span>•</span>
            <span style={{color: 'var(--accent-primary)'}}>Barrier: {insight.business_impact?.dominant_funnel_barrier || 'Uncertainty'}</span>
          </div>
        </div>
        <div>
          {isExpanded ? <ChevronUp size={20} color="var(--text-muted)" /> : <ChevronDown size={20} color="var(--text-muted)" />}
        </div>
      </div>
      
      {/* Expanded Content */}
      {isExpanded && (
        <div style={{ padding: '20px', borderTop: '1px solid var(--border-color)' }}>
          
          <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
             <span className={`badge ${severity.toLowerCase()}`}>{severity} Priority</span>
             <span className="badge" style={{background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)'}}>
               <CheckCircle2 size={14} /> AI Verified
             </span>
             {insight.scores_breakdown.cross_platform.count > 1 && (
                <span className="badge" style={{background: 'rgba(139, 92, 246, 0.1)', color: '#a78bfa'}}>
                  Cross-Platform
                </span>
             )}
          </div>
          
          <div style={{ marginBottom: '16px' }}>
            <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>AI Root Cause Analysis</h4>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', borderLeft: '3px solid var(--accent-primary)' }}>
              <AlertCircle size={18} color="var(--accent-primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <p style={{ fontSize: '0.95rem', lineHeight: '1.5' }}>
                Customers are experiencing <strong>{insight.business_impact.dominant_funnel_barrier === 'None' ? 'General Friction' : insight.business_impact.dominant_funnel_barrier}</strong>. 
                Specifically, they lack the confidence to purchase because of uncertainties regarding <strong>{insight.friction_point.replace(/ *\([^)]*\) */g, "")}</strong>. This primarily affects categories like {insight.business_impact.affected_categories.join(', ')}.
              </p>
            </div>
          </div>
          
          <div>
            <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Raw User Evidence</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {quotes.slice(0, 3).map((quote, idx) => (
                <div key={idx} style={{ display: 'flex', gap: '12px', background: 'rgba(15, 17, 23, 0.5)', padding: '12px 16px', borderRadius: '8px' }}>
                  <Quote size={16} color="var(--text-muted)" style={{ flexShrink: 0, marginTop: '4px' }} />
                  <p style={{ fontSize: '0.9rem', fontStyle: 'italic', color: 'var(--text-main)', lineHeight: '1.4' }}>"{quote}"</p>
                </div>
              ))}
            </div>
          </div>
          
        </div>
      )}
    </div>
  );
};

export default InsightDetail;
