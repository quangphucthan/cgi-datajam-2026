export const sendTriageRequest = async (message) => {
    try {
        const response = await fetch ('http://localhost:5000/api/triage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: message })
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