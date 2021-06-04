import logo from './logo.svg';
import './App.css';
import React, { useEffect } from "react";
import axios from 'axios';
import {
  Chart,
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip
} from 'chart.js';

Chart.register(
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip
);

function App() {
  const root = 'https://127.0.0.1:5045'; //set to empty string for production
  useEffect(() => {
    axios.get(root+'/water/sensors/history')
    .then(response => {
      // console.log(response.data);
      
      const ctx = document.getElementById("history");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: response.data['time_labels'],
          datasets: [
            {
              label: 'a81758fffe059fdd',
              data: response.data['a81758fffe059fdd'],
              backgroundColor: 'green',
              borderColor: 'green',
              borderWidth: 1
            },
            {
              label: 'a81758fffe059fdc',
              data: response.data['a81758fffe059fdc'],
              backgroundColor: 'blue',
              borderColor: 'blue',
              borderWidth: 1
            },
            {
              label: 'a81758fffe03e451',
              data: response.data['a81758fffe03e451'],
              backgroundColor: 'red',
              borderColor: 'red',
              borderWidth: 1
            },
          ]
        },
        options: {
          legend: {
            display: true  //doesn't work
          },
          // plugins: {
          //     title: {
          //         display: true,
          //         text: 'Historical Distance of water to sensor (smaller is more water)'
          //     }
          // }
        }
      });
    });
    axios.get(root+'/water/sensors/current')
    .then(response => {
      // console.log('curr=',response.data);

      const ctx = document.getElementById("current");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: Object.keys(response.data),
          datasets: [
            {
              label: 'toggle',
              data: Object.values(response.data),
              backgroundColor: ['red', 'blue', 'green'],
              borderColor: ['red', 'blue', 'green'],
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            y: [{
              title: {
                display: true,
                text: 'Your Title'
              }
            }]
          }
        }
      });
    });
  });
  return (
    <div className="App">
      <header className="App-header">
        <h2>Current Distance (mm) between sensor and water</h2>
        <canvas class="bar_graph" id="current" width="400" height="400"></canvas>
        <p>As water gets higher, distance will decrease. See sensor locations below.</p>
        <h2>Historical Trend in Distance of water to sensor</h2>
        <canvas class="line_graph" id="history" width="400" height="400"></canvas>
        <h2>Sensor Locations</h2>
        <img src="sensor_locations.png"></img>
        <a href="https://data-fredericton.opendata.arcgis.com/maps/29515f1fea754d23954aa4afbbb0d76d/about"
        color="white">
          Data Source
        </a>
      </header>
    </div>
  );
}

export default App;
