import React, { useState } from 'react';
import axios from 'axios';

const Prediction = () => {
  const [predictionType, setPredictionType] = useState('match'); // 'match' or 'season'
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const [team, setTeam] = useState(''); // for season prediction
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    try {
      if (predictionType === 'match') {
        const response = await axios.post('http://localhost:5000/predict/match', {
          home_team: homeTeam,
          away_team: awayTeam,
        });
        setPrediction(response.data);
      } else {
        const response = await axios.post('http://localhost:5000/predict/season', {
          team: team,
        });
        setPrediction(response.data);
      }
    } catch (error) {
      console.error('Error:', error);
      setPrediction({ error: 'Failed to get prediction' });
    }
    setLoading(false);
  };

  return (
    <div className="prediction-container">
      <h2>Football Predictions</h2>
      <div className="prediction-type-selector">
        <button
          className={predictionType === 'match' ? 'active' : ''}
          onClick={() => setPredictionType('match')}
        >
          Match Prediction
        </button>
        <button
          className={predictionType === 'season' ? 'active' : ''}
          onClick={() => setPredictionType('season')}
        >
          Season Prediction
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {predictionType === 'match' ? (
          <>
            <input
              type="text"
              placeholder="Home Team"
              value={homeTeam}
              onChange={(e) => setHomeTeam(e.target.value)}
            />
            <input
              type="text"
              placeholder="Away Team"
              value={awayTeam}
              onChange={(e) => setAwayTeam(e.target.value)}
            />
          </>
        ) : (
          <input
            type="text"
            placeholder="Team Name"
            value={team}
            onChange={(e) => setTeam(e.target.value)}
          />
        )}
        <button type="submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict'}
        </button>
      </form>

      {prediction && (
        <div className="prediction-result">
          {prediction.error ? (
            <p className="error">{prediction.error}</p>
          ) : predictionType === 'match' ? (
            <div>
              <h3>Match Prediction:</h3>
              <p>Home Team Win Probability: {prediction.home_win_prob}%</p>
              <p>Draw Probability: {prediction.draw_prob}%</p>
              <p>Away Team Win Probability: {prediction.away_win_prob}%</p>
            </div>
          ) : (
            <div>
              <h3>Season Prediction:</h3>
              <p>Predicted Position: {prediction.position}</p>
              <p>Predicted Points: {prediction.points}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Prediction;
