import React, { useState } from 'react';
import '../CSS/HomePage.css';
const HomePage = () => {
  const [prediction, setPrediction] = useState(null); // Store prediction result
  const [plot, setPlot] = useState(null); // Store the plot image
  const [loading, setLoading] = useState(false); // Loading state

  const handlePredict = async () => {
    setLoading(true); // Set loading to true while fetching
    setPrediction(null); // Reset previous prediction
    setPlot(null); // Reset previous plot

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
      });

      if (response.ok) {
        const result = await response.json();
        setPrediction(result.predicted_class); // Set predicted class
        setPlot(result.image); // Set the plot Base64 string
      } else {
        console.log('Failed to fetch prediction!');
      }
    } catch (error) {
      console.error('Error during prediction:', error);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="home-page">
      <div className="header">
        <h1>EEG Prediction System</h1>
        <p>
          This system predicts EEG signals and visualizes the output for
          better analysis.
        </p>
      </div>

      <div className="content">
        <button
          className="predict-button"
          onClick={handlePredict}
          disabled={loading}
        >
          {loading ? 'Predicting...' : 'Predict EEG'}
        </button>

        {prediction && (
          <div className="prediction-result">
            <h2>Prediction Result:</h2>
            <p className="result">{prediction}</p>
          </div>
        )}

        {plot && (
          <div className="plot-container">
            <h2>EEG Signal Visualization</h2>
            <img
              className="eeg-plot"
              src={`data:image/png;base64,${plot}`}
              alt="EEG Plot"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;

