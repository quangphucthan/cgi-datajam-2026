export const sendTriageRequest = async (message, location = null) => {
    try {
        const payload = {
            text: message,
            location: location ? { lat: location.lat, lng: location.lng } : null
        };


        const response = await fetch ('http://localhost:5000/api/triage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error sending triage request:', error);
        throw error;
    }
};