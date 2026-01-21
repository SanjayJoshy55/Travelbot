import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        { role: 'bot', content: "Hello! I'm your AI Travel Agent. Where are you planning to go?" }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [chatState, setChatState] = useState({}); // Stores conversation state (dest, days, etc.)
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!inputText.trim()) return;

        const userMsg = { role: 'user', content: inputText };
        setMessages(prev => [...prev, userMsg]);
        setInputText('');
        setIsLoading(true);

        try {
            const response = await axios.post('http://127.0.0.1:8000/chat', {
                message: userMsg.content,
                state: chatState
            });

            const botMsg = { role: 'bot', content: response.data.response };
            setMessages(prev => [...prev, botMsg]);
            setChatState(response.data.state); // Update state with backend response

        } catch (error) {
            console.error("Error sending message:", error);
            setMessages(prev => [...prev, { role: 'bot', content: "Sorry, I'm having trouble connecting to the server." }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="chat-container">
            <div className="messages-area">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        {msg.role === 'bot' ? (
                            <div className="markdown-content">
                                <ReactMarkdown>{msg.content}</ReactMarkdown>
                            </div>
                        ) : (
                            msg.content
                        )}
                    </div>
                ))}
                {isLoading && (
                    <div className="message bot">
                        <span className="typing-indicator">Thinking...</span>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Type your travel plans..."
                    disabled={isLoading}
                />
                <button className="send-btn" onClick={sendMessage} disabled={isLoading}>
                    Send ✈️
                </button>
            </div>
        </div>
    );
};

export default ChatInterface;
