import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import MapView from './components/MapView';

const App = () => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    // const [latestTriageData, setLatestTriageData] = useState(null);

    const handleSendMessage = async (text) => {
        const newMsg = {
            id: Date.now(),
            role: 'user',
            content: text,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, newMsg]);
        setIsLoading(true);
    }

    return (
        <div className="flex flex-col md:flex-row h-full w-full font-sans bg-slate-50 text-slate-900 overflow-hidden">
            {/* Left Panel: AI Triage Chat */}
            <div className="w-full md:w-[400px] lg:w-[450px] h-1/2 md:h-full flex-shrink-0 z-10 shadow-2xl transition-all duration-300">
                <ChatInterface
                    messages={messages}
                    onSendMessage={handleSendMessage}
                    isLoading={isLoading}
                />
            </div>

            {/* Right Panel: Predictive Map */}
            {/* <div className="w-full flex-1 h-1/2 md:h-full relative z-0 border-t md:border-t-0 md:border-l border-slate-300 shadow-inner">
                <MapView triageData={latestTriageData} />
            </div> */}
        </div>
    );
};

export default App;