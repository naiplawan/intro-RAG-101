import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [query, setQuery] = useState('');
    const [chatMessages, setChatMessages] = useState([]);
    const [message, setMessage] = useState('');

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleQuerySubmit = async () => {
        if (!query) {
            setMessage('Please enter a query.');
            return;
        }

        // Add user query to chat
        setChatMessages((prevMessages) => [
            ...prevMessages,
            { role: 'user', content: query },
        ]);

        try {
            const response = await axios.post('http://localhost:5000/query', { query });
            // Add response to chat
            setChatMessages((prevMessages) => [
                ...prevMessages,
                { role: 'system', content: response.data.passages.map((passage, index) => (
                    <div key={index}>
                        <h3>Source: {passage[0]}, Page: {passage[1]}</h3>
                        <p>{passage[2]}</p>
                    </div>
                )) },
            ]);
            setQuery('');
        } catch (error) {
            setMessage('Error querying passages: ' + error.message);
        }
    };

    return (
        <div className="max-w-xl mx-auto ">
            <h1 className="text-2xl font-bold mb-4">Query System</h1>

            {/* Chat Window */}
            <div className="border border-gray-300 rounded p-4 h-72 overflow-y-scroll mb-4">
                {chatMessages.map((msg, index) => (
                    <div key={index} className="my-2">
                        <div className={`font-${msg.role === 'user' ? 'bold' : 'normal'} text-${msg.role === 'user' ? 'right' : 'left'}`}>
                            {msg.role === 'user' ? 'You' : 'System'}: {msg.content}
                        </div>
                    </div>
                ))}
            </div>

            {/* Query Input */}
            <div className="flex mt-2">
                <input
                    type="text"
                    value={query}
                    onChange={handleQueryChange}
                    placeholder="Enter query"
                    className="flex-1 p-2 rounded border border-gray-300 mr-2"
                />
                <button onClick={handleQuerySubmit} className="px-4 py-2 rounded bg-blue-500 text-white border-none">
                    Send
                </button>
            </div>

            {message && <p className="mt-2 text-red-500">{message}</p>}
        </div>
    );
}

export default App;
