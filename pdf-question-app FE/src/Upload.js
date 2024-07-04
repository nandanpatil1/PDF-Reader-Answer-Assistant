import React, { useState } from 'react';
import axios from 'axios';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setMessage(response.data.message);
        } catch (error) {
            setMessage(`Error uploading file: ${error.message}`);
        }
    };

    return (
        <div className="upload-container">
            <h2>Upload PDF</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Process PDF</button>
            {message && <p className="message">{message}</p>}
        </div>
    );
};

export default Upload;
