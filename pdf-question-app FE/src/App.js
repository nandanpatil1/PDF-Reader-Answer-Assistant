import React from 'react';
import './App.css';
import Upload from './Upload';
import Question from './Question';

const App = () => {
    return (
        <div className="app-container">
            <div className="left-panel">
                <div className="logo">
                    <img src="logo.png" alt="Logo" />
                </div>
                <Upload />
            </div>
            <div className="right-panel">
                <Question />
            </div>
        </div>
    );
};

export default App;
