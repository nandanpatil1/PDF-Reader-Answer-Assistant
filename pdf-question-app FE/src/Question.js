import React, { useState } from 'react';
import axios from 'axios';

const Question = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [message, setMessage] = useState('');

    const handleQuestionChange = (event) => {
        setQuestion(event.target.value);
    };

    const handleAskQuestion = async () => {
        try {
            const response = await axios.post('http://localhost:8000/question/', { question });

            if (response.status === 200) {
                setAnswer(response.data.answer);
                setMessage('Answer found:');
            } else {
                setAnswer('No answer found.');
                setMessage('No answer found.');
            }
        } catch (error) {
            setAnswer(`Error asking question: ${error.message}`);
            setMessage('Error asking question.');
        }
    };

    return (
        <div className="question-container">
            <h2>Ask a Question</h2>
            <input type="text" value={question} onChange={handleQuestionChange} placeholder="Type your question here" />
            <button onClick={handleAskQuestion}>Ask</button>
            {message && <p className={`message ${message.includes('Answer found') ? 'success' : 'error'}`}>{message}</p>}
            {answer && <p className={`answer ${answer.includes('No answer') || answer.includes('Error') ? 'error' : 'success'}`}>{answer}</p>}
        </div>
    );
};

export default Question;
