import React, { useState } from 'react';
import axios from 'axios';
import './Video.css';
import { motion } from 'framer-motion';

function VideoUpload() {
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState([]);
  const [advice, setAdvice] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select a video file first.");
      return;
    }
    setLoading(true);
    setError('');
    setAdvice('');
    setFeedback([]);
    setSummary('');
    const formData = new FormData();
    formData.append("video", file);
    try {
      const res = await axios.post("http://localhost:5000/analyze", formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setFeedback(res.data.bad_postures || []);
      setAdvice(res.data.advice || '');
      setSummary(res.data.summary || '');
    } catch (err) {
      setError("Failed to upload or process the video. Please try again.");
    }
    setLoading(false);
  };

  return (
    <motion.div
      className="upload-container"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <h2 className="title">Upload Your Posture Video</h2>

      <div className="button-group">
        <label className="file-label">
          <input
            type="file"
            accept="video/*"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setError('');
              setAdvice('');
              setFeedback([]);
              setSummary('');
            }}
            className="file-input"
          />
          <span className="file-custom">Choose File</span>
        </label>

        <motion.button
          className="upload-btn"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          transition={{ type: "spring", stiffness: 300 }}
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Upload & Analyze'}
        </motion.button>
      </div>

      {file && <p className="selected-file">Selected: {file.name}</p>}
      {error && <p className="error-text">{error}</p>}

      {summary && (
        <motion.div className="summary" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.6 }}>
          <strong>Summary:</strong> {summary}
        </motion.div>
      )}

      {advice && (
        <motion.div className="advice" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.6 }}>
          <strong>Advice:</strong> {advice}
        </motion.div>
      )}

      {feedback.length > 0 && (
        <div className="results">
          <h3>Frame Feedback</h3>
          <ul>
            {feedback.map((item, index) => (
              <motion.li key={index} initial={{ x: -20, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: index * 0.03 }}>
                {item}
              </motion.li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

export default VideoUpload;
