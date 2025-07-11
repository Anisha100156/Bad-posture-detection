import React from 'react';
import VideoUpload from './components/Video';

function App() {
  return (
    <div style={{ textAlign: 'center', paddingTop: '2rem' }}>
      <h1 className="app-heading">Bad Posture Detection App</h1>
      <VideoUpload />
    </div>
  );
}

export default App;
