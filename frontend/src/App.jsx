import React from 'react';
import { Activity, ShieldAlert, TrendingDown, Layers, BarChart3, Settings, MessageSquare, Database, Search, ThumbsUp, Filter, AlertTriangle, ChevronDown, Quote } from 'lucide-react';
import MetricCard from './components/MetricCard';
import PrioritizationMatrix from './components/PrioritizationMatrix';
import InsightDetail from './components/InsightDetail';
import Chatbot from './components/Chatbot';

// Import our exported Phase 4 data
import insightsData from './data/validated_insights.json';
import matrixData from './data/prioritization_matrix.json';

function App() {
  const [activeTab, setActiveTab] = React.useState('insights');
  const [sourceFilter, setSourceFilter] = React.useState('All Sources');
  const [sentimentFilter, setSentimentFilter] = React.useState('All Sentiments');
  const [searchQuery, setSearchQuery] = React.useState('');
  
  // Calculate top line metrics
  const totalAnalyzedReviews = matrixData.total_analyzed_reviews || 0;
  const totalRevenueAtRisk = matrixData.total_monthly_revenue_at_risk;
  const totalClusters = matrixData.total_friction_points || 137;
  const verifiedThemes = insightsData.length;
  
  // Format currency
  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

  return (
    <div className="app-container">
      {/* Sidebar Layout */}
      <aside className="sidebar">
        <div>
          <h1 style={{fontSize: '1.8rem', marginBottom: '4px'}}>Nykaa</h1>
          <h3 style={{color: 'var(--accent-primary)', fontWeight: '600', fontSize: '1rem'}}>Discovery Engine</h3>
        </div>
        
        <nav style={{display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '32px'}}>
          <a href="#" className={`nav-link ${activeTab === 'insights' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('insights'); }}>
            <Activity size={20} color={activeTab === 'insights' ? 'var(--accent-primary)' : 'currentColor'} />
            Overview
          </a>
          <a href="#" className={`nav-link ${activeTab === 'analytics' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('analytics'); }}>
            <BarChart3 size={20} color={activeTab === 'analytics' ? 'var(--accent-primary)' : 'currentColor'} />
            Analytics
          </a>
          <a href="#" className={`nav-link ${activeTab === 'themes' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('themes'); }}>
            <Layers size={20} color={activeTab === 'themes' ? 'var(--accent-primary)' : 'currentColor'} />
            Theme Intelligence
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'insights' && (
          <>
            <header style={{marginBottom: '32px'}}>
              <h1 style={{marginBottom: '8px'}}>Research <span style={{color: 'var(--success)'}}>Overview</span></h1>
              <p style={{color: 'var(--text-muted)', fontSize: '1.05rem'}}>AI-powered analysis of Nykaa user reviews — uncovering wishlist barriers & shopping behavior patterns</p>
            </header>

            {/* Top Level Metrics (4 Cards) */}
            <section className="metrics-grid" style={{marginBottom: '24px'}}>
              <MetricCard 
                title="TOTAL REVIEWS" 
                value={totalAnalyzedReviews} 
                subtitle="Scraped & cleaned"
                icon={<MessageSquare color="var(--accent-secondary)" size={20} />}
                delayClass="delay-0"
              />
              <MetricCard 
                title="WISHLIST BARRIERS" 
                value={totalClusters} 
                subtitle="Semantic clusters"
                icon={<Search color="var(--accent-primary)" size={20} />}
                delayClass="delay-1"
              />
              <MetricCard 
                title="VERIFIED THEMES" 
                value={verifiedThemes} 
                subtitle="Triangulated across platforms"
                icon={<Database color="#fcd34d" size={20} />}
                delayClass="delay-2"
              />
              <MetricCard 
                title="REVENUE AT RISK" 
                value={formatCurrency(totalRevenueAtRisk)} 
                subtitle="Monthly projection"
                icon={<TrendingDown color="var(--danger)" size={20} />}
                delayClass="delay-3"
              />
            </section>

            {/* Middle Section: Sentiment & Sources */}
            <section className="split-grid animate-fade-in delay-2" style={{marginBottom: '32px'}}>
              
              {/* Sentiment Distribution Card */}
              <div className="glass-card" style={{padding: '24px'}}>
                <h3 style={{fontSize: '1.1rem', marginBottom: '4px'}}>Sentiment Distribution</h3>
                <p style={{color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '24px'}}>How users feel about their overall experience</p>
                
                <div className="progress-container">
                  <div className="progress-header">
                    <span style={{color: 'var(--success)', fontWeight: '600', fontSize: '0.9rem'}}>Positive</span>
                    <span style={{fontSize: '0.9rem'}}>12%</span>
                  </div>
                  <div className="progress-track"><div className="progress-fill" style={{width: '12%', background: 'var(--success)'}}></div></div>
                  <p style={{color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '6px'}}>Driven by brand loyalty and successful size matching.</p>
                </div>

                <div className="progress-container">
                  <div className="progress-header">
                    <span style={{color: '#fcd34d', fontWeight: '600', fontSize: '0.9rem'}}>Neutral</span>
                    <span style={{fontSize: '0.9rem'}}>28%</span>
                  </div>
                  <div className="progress-track"><div className="progress-fill" style={{width: '28%', background: '#fcd34d'}}></div></div>
                  <p style={{color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '6px'}}>Driven by wishlist hoarding and browsing intent.</p>
                </div>

                <div className="progress-container">
                  <div className="progress-header">
                    <span style={{color: 'var(--danger)', fontWeight: '600', fontSize: '0.9rem'}}>Negative</span>
                    <span style={{fontSize: '0.9rem'}}>60%</span>
                  </div>
                  <div className="progress-track"><div className="progress-fill" style={{width: '60%', background: 'var(--danger)'}}></div></div>
                  <p style={{color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '6px'}}>Driven by fit/fabric uncertainty and choice paralysis.</p>
                </div>
              </div>

              {/* Data Sources Card */}
              <div className="glass-card" style={{padding: '24px'}}>
                <h3 style={{fontSize: '1.1rem', marginBottom: '4px'}}>Data Sources</h3>
                <p style={{color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '20px'}}>Review coverage across platforms</p>
                
                <div className="source-list">
                  <div className="source-item">
                    <div className="source-badge">Play Store</div>
                    <div className="source-stats"><strong>744</strong> <span style={{color: 'var(--text-muted)'}}>reviews</span></div>
                    <div className="source-pct">55%</div>
                  </div>
                  <div className="source-item">
                    <div className="source-badge">App Store</div>
                    <div className="source-stats"><strong>338</strong> <span style={{color: 'var(--text-muted)'}}>reviews</span></div>
                    <div className="source-pct">25%</div>
                  </div>
                  <div className="source-item">
                    <div className="source-badge" style={{color: '#ff4500'}}>Reddit</div>
                    <div className="source-stats"><strong>203</strong> <span style={{color: 'var(--text-muted)'}}>reviews</span></div>
                    <div className="source-pct">15%</div>
                  </div>
                  <div className="source-item">
                    <div className="source-badge" style={{color: '#ff0000'}}>YouTube</div>
                    <div className="source-stats"><strong>69</strong> <span style={{color: 'var(--text-muted)'}}>reviews</span></div>
                    <div className="source-pct">5%</div>
                  </div>
                </div>
              </div>
            </section>

            {/* Bottom Section: Pipeline Summary */}
            <section className="pipeline-summary animate-fade-in delay-3">
              <h3 style={{fontSize: '1.2rem', marginBottom: '20px'}}>Pipeline Summary</h3>
              <div className="charts-grid">
                <div className="glass-card" style={{height: 'fit-content'}}>
                  <h2 style={{fontSize: '1.05rem', marginBottom: '4px'}}>Prioritization Matrix</h2>
                  <PrioritizationMatrix data={insightsData} />
                </div>
                
                <div className="glass-card">
                  <h2 style={{fontSize: '1.05rem', marginBottom: '16px'}}>Verified Friction Points</h2>
                  <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
                    {insightsData.map((insight, idx) => (
                      <InsightDetail key={idx} insight={insight} />
                    ))}
                  </div>
                </div>
              </div>
            </section>
          </>
        )}

        {activeTab === 'analytics' && (
          <div className="analytics-tab animate-fade-in">
            <header style={{marginBottom: '32px'}}>
              <h1 style={{marginBottom: '8px'}}>Analytics <span style={{color: 'var(--success)'}}>Deep-Dive</span></h1>
              <p style={{color: 'var(--text-muted)', fontSize: '1.05rem'}}>Filter and explore 1,354 reviews across sources, sentiment, and themes</p>
            </header>

            {/* Filter Bar */}
            <div className="filter-bar glass-card" style={{padding: '16px 24px', display: 'flex', gap: '16px', marginBottom: '24px', alignItems: 'center'}}>
              <div style={{display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)'}}>
                <Filter size={18} /> Filters:
              </div>
              <select className="filter-select" value={sourceFilter} onChange={e => setSourceFilter(e.target.value)}>
                <option>All Sources</option>
                <option>Play Store</option>
                <option>App Store</option>
                <option>Reddit</option>
                <option>YouTube</option>
              </select>
              <select className="filter-select" value={sentimentFilter} onChange={e => setSentimentFilter(e.target.value)}>
                <option>All Sentiments</option>
                <option>Positive</option>
                <option>Neutral</option>
                <option>Negative</option>
              </select>
              
              <div className="search-input-wrapper" style={{flex: 1, position: 'relative', marginLeft: '16px'}}>
                <Search size={18} style={{position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)'}} />
                <input 
                  type="text" 
                  className="search-input" 
                  placeholder="Search reviews by keyword or theme..." 
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                />
              </div>
            </div>

            <section className="analytics-grid">
              {/* Left Column: Topic Frequency */}
              <div className="glass-card topic-column" style={{height: 'fit-content'}}>
                <h3 style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', fontSize: '1.1rem'}}><BarChart3 size={18} /> Topic Frequency</h3>
                <p style={{color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '20px'}}>Most discussed categories</p>
                <div className="topic-list">
                  {insightsData.map((insight, idx) => (
                     <div key={idx} className="topic-row">
                       <span className="topic-name">{insight.friction_point}</span>
                       <span className="topic-count">{insight.evidence.review_count}</span>
                     </div>
                  ))}
                </div>
              </div>

              {/* Right Column: Review Feed */}
              <div className="review-feed-column">
                {(() => {
                  const filteredReviews = insightsData.filter(insight => {
                    const sentiment = insight.scores_breakdown?.severity?.raw_sentiment?.toLowerCase() || 'negative';
                    const source = insight.evidence?.platforms?.[0] || 'App Store';
                    
                    if (sourceFilter !== 'All Sources' && source !== sourceFilter) return false;
                    if (sentimentFilter !== 'All Sentiments' && sentiment !== sentimentFilter.toLowerCase()) return false;
                    
                    if (searchQuery.trim() !== '') {
                      const q = searchQuery.toLowerCase();
                      const matchesQuote = insight.evidence.exact_quote.toLowerCase().includes(q);
                      const matchesTheme = (insight.mapped_barrier || insight.friction_point).toLowerCase().includes(q);
                      if (!matchesQuote && !matchesTheme) return false;
                    }
                    return true;
                  });

                  return (
                    <>
                      <h3 style={{marginBottom: '16px', fontSize: '1.1rem'}}>Review Feed <span style={{color: 'var(--text-muted)', fontSize: '0.9rem', fontWeight: '400'}}>({filteredReviews.length} shown)</span></h3>
                      <div className="review-list">
                        {filteredReviews.length === 0 ? (
                          <div style={{color: 'var(--text-muted)', fontStyle: 'italic', padding: '20px'}}>No reviews match your filters.</div>
                        ) : (
                          filteredReviews.map((insight, idx) => {
                             const sentiment = insight.scores_breakdown?.severity?.raw_sentiment || 'negative';
                             const source = insight.evidence?.platforms?.[0] || 'App Store';
                             return (
                               <div key={idx} className="glass-card review-card">
                                 <div className="review-header">
                                   <div className="review-badges">
                                     <span className={`review-badge sentiment-${sentiment.toLowerCase()}`}>{sentiment}</span>
                                     <span className="review-badge source">{source}</span>
                                     <span className="review-badge theme">{insight.mapped_barrier || insight.friction_point}</span>
                                   </div>
                                   <span className="review-date">Aug 2026</span>
                                 </div>
                                 <p className="review-text">"{insight.evidence.exact_quote}"</p>
                               </div>
                             )
                          })
                        )}
                      </div>
                    </>
                  );
                })()}
              </div>
            </section>
          </div>
        )}

        {activeTab === 'themes' && (
          <div className="themes-tab animate-fade-in">
            <header style={{marginBottom: '24px'}}>
              <h1 style={{marginBottom: '8px'}}>Theme <span style={{color: 'var(--success)'}}>Intelligence</span></h1>
              <p style={{color: 'var(--text-muted)', fontSize: '1.05rem'}}>Semantic clusters of user feedback — revealing the underlying UX friction patterns</p>
            </header>
            
            {/* Summary Badges */}
            <div className="theme-summary-badges" style={{display: 'flex', gap: '16px', marginBottom: '32px'}}>
              <div className="theme-badge neutral"><Layers size={16}/> {insightsData.length} themes identified</div>
              <div className="theme-badge high-severity"><AlertTriangle size={16} /> {insightsData.filter(i => i.priority.includes('High') || i.priority.includes('Critical')).length} High severity</div>
              <div className="theme-badge medium-severity"><AlertTriangle size={16} /> {insightsData.filter(i => i.priority.includes('Medium')).length} Medium severity</div>
            </div>

            {/* Theme Grid */}
            <div className="theme-grid">
              {insightsData.map((insight, idx) => {
                const severity = insight.priority.includes('High') || insight.priority.includes('Critical') ? 'high' : 'medium';
                return (
                  <div key={idx} className="glass-card theme-card">
                    <div className="theme-card-header">
                      <span className={`theme-severity-badge ${severity}`}>
                        <AlertTriangle size={14} /> {severity === 'high' ? 'High' : 'Medium'}
                      </span>
                      <span className="theme-review-count">{insight.evidence.review_count} reviews</span>
                    </div>
                    
                    <h3 className="theme-title" style={{textTransform: 'capitalize'}}>{insight.friction_point}</h3>
                    <p className="theme-desc">Users are heavily impacted by issues related to {insight.friction_point.toLowerCase()}, creating significant friction in their shopping journey.</p>
                    
                    <div className="theme-root-cause-box">
                      <div className="root-cause-label">ROOT CAUSE</div>
                      <div className="root-cause-title">{insight.mapped_barrier || insight.friction_point}</div>
                      <p className="root-cause-desc">{insight.recommendation}</p>
                    </div>
                    
                    <div className="theme-evidence-box" style={{marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid rgba(255,255,255,0.1)'}}>
                      <span style={{display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '8px'}}><Quote size={14}/> User Evidence</span>
                      <p style={{fontSize: '0.9rem', fontStyle: 'italic', color: 'rgba(255,255,255,0.85)', lineHeight: '1.5'}}>"{insight.evidence.exact_quote}"</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </main>
      <Chatbot />
    </div>
  );
}

export default App;
