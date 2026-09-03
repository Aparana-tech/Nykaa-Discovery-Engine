import React, { useState, useRef, useEffect } from 'react';
import insightsData from '../data/validated_insights.json';
import matrixData from '../data/prioritization_matrix.json';

const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I am the Nykaa Discovery AI. I can answer any questions about our analyzed reviews and friction points. What would you like to know?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const suggestedQuestions = [
    "What prevents wishlisted products from being purchased?",
    "Which user segments drop off the most and why?",
    "Are these UI/UX issues or product issues?",
    "What is the total revenue at risk?"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (text) => {
    if (!text.trim()) return;
    
    const userMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const systemPrompt = `
      You are an expert AI Assistant built by the Nykaa Fashion Data Science team.
      Your goal is to answer questions about the Nykaa Fashion Discovery Engine project.
      Here is the exact data we processed from user reviews:
      
      Insights Data:
      ${JSON.stringify(insightsData, null, 2)}
      
      Prioritization Matrix:
      ${JSON.stringify(matrixData, null, 2)}
      
      CRITICAL INSTRUCTION: Keep your answers concise and informative. Aim for 3 to 4 well-structured sentences. 
      Get straight to the point without any fluff. Directly reference the data when possible.
      Format your response with standard markdown (bolding).
      `;

      // Convert our chat history to Gemini's format
      const contents = messages.filter(m => m.role !== 'system').map(m => ({
        role: m.role === 'assistant' ? 'model' : 'user',
        parts: [{ text: m.content }]
      }));
      
      // Add the new user message
      contents.push({
        role: 'user',
        parts: [{ text: text }]
      });

      let retries = 3;
      let response;
      let data;
      
      while (retries > 0) {
        response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=${GEMINI_API_KEY}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            systemInstruction: {
              parts: [{ text: systemPrompt }]
            },
            contents: contents,
            generationConfig: {
              temperature: 0.2
            }
          })
        });

        data = await response.json();
        
        if (response.status === 429) {
          console.warn("Rate limit hit, retrying in 4 seconds...");
          await new Promise(r => setTimeout(r, 4000));
          retries--;
        } else {
          break;
        }
      }
      
      if (data.error) {
        throw new Error(data.error.message || "Unknown API error");
      }
      
      const botResponse = data.candidates[0].content.parts[0].text;
      
      setMessages(prev => [...prev, { role: 'assistant', content: botResponse }]);
    } catch (error) {
      console.error("Chatbot Error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "I'm currently experiencing high traffic and cannot connect to the server right now. Please try again in a few moments." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend(input);
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <button 
        className={`chatbot-fab ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle Chatbot"
      >
        {isOpen ? (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        ) : (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        )}
      </button>

      {/* Floating Label */}
      {!isOpen && (
        <div 
          onClick={() => setIsOpen(true)}
          style={{
            position: 'fixed',
            bottom: '42px',
            left: '105px',
            background: 'var(--primary)', 
            color: 'white', 
            padding: '8px 16px', 
            borderRadius: '20px', 
            fontWeight: '600', 
            fontSize: '0.95rem',
            cursor: 'pointer',
            boxShadow: '0 4px 15px rgba(232, 0, 113, 0.4)',
            zIndex: 1000,
            animation: 'fadeIn 0.5s ease',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          Ask Me Questions 
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </div>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div>
              <h3>Ask Me Questions</h3>
              <span className="status">● Online</span>
            </div>
          </div>
          
          <div className="chatbot-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-bubble">
                  {msg.content.split('\\n').map((line, i) => <p key={i}>{line}</p>)}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-bubble typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-suggestions">
            {messages.length === 1 && suggestedQuestions.map((q, idx) => (
              <button key={idx} onClick={() => handleSend(q)} className="suggestion-btn">
                {q}
              </button>
            ))}
          </div>

          <div className="chatbot-input">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask me anything..."
              rows="1"
            />
            <button onClick={() => handleSend(input)} disabled={!input.trim() || isLoading}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </div>
        </div>
      )}
    </>
  );
}
