import React from 'react';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const ResultsScreen = () => {
  const metrics = [
    { name: 'Walkability Score', value: "Add call to walkability API" },
    { name: 'Weather Score', value: "Add cal to weather score API" },
    { name: 'Disaster Score', value: "add call to disaster API" },
    { name: 'ADD dataBase score here!', value: "add call to the new API" },
  ];

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Weather Event Metrics</h1>
      <div style={styles.metricsContainer}>
        {metrics.map((metric, index) => (
          <div key={index} style={styles.metricItem}>
            <h3 style={styles.metricName}>{metric.name}</h3>
            <div style={styles.progressBarContainer}>
              <CircularProgressbar
                value={metric.value}
                text={`${metric.value}%`}
                styles={{
                  path: { stroke: `rgba(62, 152, 199, ${metric.value / 100})` },
                  text: { fill: '#333', fontSize: '16px' },
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    textAlign: 'center',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  title: {
    fontSize: '2rem',
    marginBottom: '20px',
    color: '#333',
  },
  metricsContainer: {
    display: 'flex',
    justifyContent: 'space-around',
    flexWrap: 'wrap',
  },
  metricItem: {
    width: '200px',
    margin: '10px',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#f9f9f9',
  },
  metricName: {
    fontSize: '1.2rem',
    marginBottom: '10px',
    color: '#555',
  },
  progressBarContainer: {
    width: '100px',
    height: '100px',
    margin: '0 auto',
  },
};

export default ResultsScreen;