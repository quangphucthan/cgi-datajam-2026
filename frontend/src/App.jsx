import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import MapView from './components/MapView';
import HospitalCard from './components/HospitalCard';
import { sendTriageRequest } from './services/service';

const App = () => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [latestTriageData, setLatestTriageData] = useState(null);

    // Mock hospital data based on CSV structure
    const mockHospitals = [
        {
            facility: "Halifax Infirmary (QEII)",
            address: "1796 Summer Street",
            town: "Halifax",
            county: "Halifax",
            type: "regional",
            the_geom: "POINT(-63.5714 44.6488)"
        },
        {
            facility: "Dartmouth General Hospital",
            address: "325 Pleasant Street",
            town: "Dartmouth",
            county: "Halifax",
            type: "regional",
            the_geom: "POINT(-63.5156 44.6688)"
        },
        {
            facility: "IWK Health Centre",
            address: "5850/5980 University Avenue",
            town: "Halifax",
            county: "Halifax",
            type: "regional",
            the_geom: "POINT(-63.5920 44.6361)"
        },
        {
            facility: "Cobequid Community Health Centre",
            address: "40 Freer Lane",
            town: "Lower Sackville",
            county: "Halifax",
            type: "community",
            the_geom: "POINT(-63.6789 44.7765)"
        }
    ];

    const handleSendMessage = async (text) => {
        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: text,
            timestamp: new Date()
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        // send request to backend
        try {
            const triageData = await sendTriageRequest(text);
            setLatestTriageData(triageData);

            const modelMessage = {
                id: Date.now() + 1,
                role: 'model',
                content: triageData.reply || 'No debug reply returned.',
                triageData,
                timestamp: new Date()
            };

            setMessages((prev) => [...prev, modelMessage]);
        } catch (error) {
            const errorMessage = {
                id: Date.now() + 1,
                role: 'model',
                content: 'I could not reach the triage service right now. Please try again in a moment.',
                timestamp: new Date()
            };

            setMessages((prev) => [...prev, errorMessage]);
            console.error('Triage request failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

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

            {/* Right Panel: Hospital Recommendations */}
            <div className="w-full flex-1 h-1/2 md:h-full relative z-0 border-t md:border-t-0 md:border-l border-slate-300 shadow-inner p-4 flex flex-col" style={{ backgroundImage: 'linear-gradient(90deg, rgba(148, 163, 184, 0.1) 1px, transparent 1px), linear-gradient(0deg, rgba(148, 163, 184, 0.1) 1px, transparent 1px)', backgroundSize: '20px 20px' }}>
                <div className="flex-shrink-0">
                    <h2 className="text-xl font-bold text-slate-800 mb-4">Recommended Facilities</h2>
                    <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2 mb-4">
                        {mockHospitals.map((hospital, index) => (
                            <HospitalCard key={index} {...hospital} />
                        ))}
                    </div>
                </div>

                <div className="flex-grow"></div>

                {/* Informational Cards - Always at bottom */}
                <div className="flex-shrink-0 mt-4">
                    <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-3">
                        {/* CTAS Levels Card */}
                        <div className="bg-white rounded-lg shadow-md p-4 border border-slate-200">
                            <h3 className="font-bold text-lg text-slate-800 mb-3 flex items-center">
                                <i className="fas fa-exclamation-triangle text-red-500 mr-2"></i>
                                CTAS Levels
                            </h3>
                            <div className="space-y-2 text-sm">
                                <div className="flex items-center">
                                    <span className="w-6 h-6 bg-red-600 text-white text-xs font-bold rounded-full flex items-center justify-center mr-2">1</span>
                                    <span className="text-slate-700">Resuscitation - Life threatening</span>
                                </div>
                                <div className="flex items-center">
                                    <span className="w-6 h-6 bg-yellow-500 text-white text-xs font-bold rounded-full flex items-center justify-center mr-2">2</span>
                                    <span className="text-slate-700">Emergent - Serious condition</span>
                                </div>
                                <div className="flex items-center">
                                    <span className="w-6 h-6 bg-orange-500 text-white text-xs font-bold rounded-full flex items-center justify-center mr-2">3</span>
                                    <span className="text-slate-700">Urgent - Needs timely care</span>
                                </div>
                                <div className="flex items-center">
                                    <span className="w-6 h-6 bg-green-600 text-white text-xs font-bold rounded-full flex items-center justify-center mr-2">4</span>
                                    <span className="text-slate-700">Less Urgent - Can wait</span>
                                </div>
                                <div className="flex items-center">
                                    <span className="w-6 h-6 bg-blue-400 text-slate-800 text-xs font-bold rounded-full flex items-center justify-center mr-2">5</span>
                                    <span className="text-slate-700">Non-Urgent - Self-care or pharmacy</span>
                                </div>
                            </div>
                        </div>

                        {/* Family Doctors Card */}
                        <div className="bg-white rounded-lg shadow-md p-4 border border-slate-200">
                            <h3 className="font-bold text-lg text-slate-800 mb-3 flex items-center">
                                <i className="fas fa-user-md text-blue-500 mr-2"></i>
                                Family Doctors
                            </h3>
                            <p className="text-sm text-slate-600 mb-2">
                                Family doctors (GPs) provide primary care for routine health needs, preventive care, and manage chronic conditions.
                            </p>
                            <p className="text-sm text-slate-600 mb-3">
                                <strong>How to get one:</strong> Register with a family practice through your provincial health plan. Many communities have walk-in clinics while you search.
                            </p>
                            <a href="https://www.nshealth.ca/family-doctors" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                                Find a Family Doctor →
                            </a>
                        </div>

                        {/* Insurance Resources Card */}
                        <div className="bg-white rounded-lg shadow-md p-4 border border-slate-200">
                            <h3 className="font-bold text-lg text-slate-800 mb-3 flex items-center">
                                <i className="fas fa-shield-alt text-green-500 mr-2"></i>
                                Health Insurance
                            </h3>
                            <p className="text-sm text-slate-600 mb-2">
                                Nova Scotia has universal healthcare through Medicare. International students may need supplemental coverage.
                            </p>
                            <div className="space-y-1 text-sm">
                                <a href="https://www.nshealth.ca/medicare" target="_blank" rel="noopener noreferrer" className="block text-blue-600 hover:text-blue-800">Medicare Information</a>
                                <a href="https://www.canada.ca/en/services/health.html" target="_blank" rel="noopener noreferrer" className="block text-blue-600 hover:text-blue-800">Federal Health Resources</a>
                                <a href="https://www.nshealth.ca/international" target="_blank" rel="noopener noreferrer" className="block text-blue-600 hover:text-blue-800">International Visitor Insurance</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
};

export default App;
