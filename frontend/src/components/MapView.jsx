import React from "react";

const MapView = ({ triageData }) => {
    return (
        <div className="h-full w-full bg-slate-200 flex items-center justify-center text-slate-500 border-l border-slate-300">
            <div className="text-center p-6 bg-white rounded-xl shadow-sm border border-slate-200">
                <i className="fas fa-map-marked-alt text-4xl mb-3 text-slate-400"></i>
                <h3 className="font-bold text-slate-700">Map View Placeholder</h3>
                <p className="text-sm mt-2">
                    {triageData
                        ? `Waiting to map facility type: ${triageData.facilityType}`
                        : "Submit symptoms in the chat to see routing."}
                </p>
            </div>
        </div>
    );
};

export default MapView;