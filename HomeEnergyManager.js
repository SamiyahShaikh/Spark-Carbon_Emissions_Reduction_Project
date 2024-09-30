import React, { useState, useEffect } from 'react';
import axios from 'axios';

const HomeEnergyManager = () => {
  const [forecastedEmissions, setForecastedEmissions] = useState([]);
  const [optimalUsage, setOptimalUsage] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch the emissions forecast and optimal usage schedule from backend
  useEffect(() => {
    async function fetchData() {
      try {
        const forecastRes = await axios.get('/api/forecast');
        setForecastedEmissions(forecastRes.data);

        const usageRes = await axios.get('/api/optimal-usage');
        setOptimalUsage(usageRes.data);
      } catch (err) {
        setError("Failed to fetch data");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Home Energy Management</h1>
      <div>
        <h2>Forecasted Carbon Emissions</h2>
        <ul>
          {forecastedEmissions.map((emission, index) => (
            <li key={index}>Day {index + 1}: {emission} kg CO2</li>
          ))}
        </ul>
      </div>

      <div>
        <h2>Optimal Energy Usage Schedule</h2>
        <ul>
          {optimalUsage.map((usage, index) => (
            <li key={index}>Day {index + 1}: {usage} kWh</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default HomeEnergyManager;
