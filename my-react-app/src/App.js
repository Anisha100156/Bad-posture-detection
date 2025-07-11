import React, { useEffect } from 'react';
import VideoUpload from './components/Video';

function App() {
  useEffect(() => {
    // Optional: Test if Flask backend is reachable
    fetch("http://localhost:5000/analyze")
      .then(res => res.json())
      .then(data => console.log("Response from Flask:", data))
      .catch(err => console.error("Error reaching Flask API:", err));
  }, []);

  return (
    <div style={{ textAlign: 'center', paddingTop: '2rem' }}>
      <h1 className="app-heading">Bad Posture Detection App</h1>
      <VideoUpload />
    </div>
  );
}

export default App;
