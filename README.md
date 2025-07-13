Machine Health Monitoring System
This project implements a Machine Health Monitoring System using multiple ESP32 boards. It gathers temperature, humidity, and sound level data from sensor nodes and sends it wirelessly to a central hub using ESP-NOW. The hub visualizes real-time sensor data on a web dashboard and uploads it to Google Sheets for remote logging and machine health status prediction using Machine Learning (Random Forest).

Features
ESP-NOW Communication between sensor nodes and hub

Web Dashboard with live charts using Chart.js

Google Sheets Integration via Google Apps Script

Health Status Evaluation & ML-Based Prediction

Real-time HTML Interface hosted on the hub

Automated Model Refresh with APScheduler

Cloud Logging & Prediction using Google Colab and Flask

Hardware Used
ESP32 Development Boards (at least 2: one hub, one or more nodes)

DHT11 Sensor for temperature and humidity

Analog Sound Sensor (connected to analog input pin)

Wi-Fi Access Point for hosting dashboard and uploading to cloud

machine-health-monitor/
├── /hub/
│   └── hub_code.ino            → Receives ESP-NOW data, serves dashboard, uploads to Google Sheets
├── /node/
│   └── node_code.ino           → Sends DHT + sound data to the hub using ESP-NOW
├── /mac_reader/
│   └── get_mac_address.ino     → Use this to retrieve ESP32 MAC addresses
├── /google_script/
│   └── code.gs                 → Google Apps Script to log data in Google Sheets
├── /ml_colab/
│   ├── predict_app.ipynb       → Google Colab notebook with Flask API & Random Forest model
│   └── data/                   → Folder for aggregated CSVs (hourly, weekly, etc.)
└── README.md

How It Works
1. Sensor Node (ESP32)
Reads temperature and humidity using DHT11

Reads sound level via analog input

Sends this data wirelessly via ESP-NOW to the hub ESP32

2. Hub ESP32
Receives data from multiple sender nodes

Displays live readings on a web dashboard (port 80)

Uploads data to Google Sheets via a GET request to Apps Script

Can optionally forward data to a Flask ML API for health prediction

3. Machine Learning API (Google Colab)
A Flask server runs in Colab, hosting a Random Forest classifier

The model:

Reads recent sensor data from Google Sheets or uploaded CSVs

Predicts machine health status: Normal / Warning / Critical

Refreshes the model every 10 minutes using APScheduler

The ESP32 hub fetches the ML prediction and updates the dashboard accordingly

4. Google Sheet
Logs each data entry with:

Timestamp

Temperature

Humidity

Sound Level

Health Status (via threshold or ML)

Can be exported as CSV for training new ML models

Machine Learning Integration
Model
Model: Random Forest Classifier

Input Features: Temperature, Humidity, Sound

Output Label: Machine Health (Normal / Warning / Critical)

Preprocessing: Handled in Colab via pandas & scikit-learn

Data Sources: Live sensor values (real-time) + Aggregated CSVs

Prediction Flow
ESP32 hub logs data to Google Sheets

Colab Flask App periodically reads the sheet & CSVs

Model predicts health status

Flask API provides predictions to ESP32 hub

Prediction is shown on the live dashboard

Web Dashboard (ESP32)
The hub’s web interface shows:

Live sensor readings (updated every 5s)

Machine status based on ML predictions

Color-coded indicators:

🟢 Normal

🟡 Warning

🔴 Critical

Google Sheets Logging
Deployment Steps:
Open code.gs in Google Apps Script

Deploy as Web App, set access to "Anyone"

Copy Web App URL and paste it into hub_code.ino

Format Sheet columns: Time | Temp | Humidity | Sound | Status

Health Status Logic (ML + Thresholds)
Metric	Threshold / ML Input	Status
Temperature	> 45°C	🔴 Critical
Humidity	< 30% or > 80%	⚠Warning / 🔴 Critical
Sound Level	> 60 (analog)	⚠Warning / 🔴 Critical
ML Model	Uses all 3	 Final Health Status

You can switch between threshold-based and ML-based prediction.

 Sample Google Sheet Entry
Time	Temp (°C)	Humidity (%)	Sound	Health Status
2025-07-12 14:20:00	42.0	60	50	Normal
2025-07-12 14:25:00	48.5	85	65	Critical

 Setup Instructions
Flash get_mac_address.ino on each ESP32 to get MAC addresses

Update sender MACs in hub_code.ino, and hub MAC in node_code.ino

Deploy Google Apps Script and update its URL in hub_code.ino

Upload node_code.ino to all sensor ESP32s

Upload hub_code.ino to the receiver ESP32

Open ESP32’s IP address in browser to view live dashboard

Run predict_app.ipynb on Google Colab to start ML Flask server

Copy Flask endpoint URL and configure hub to fetch predictions

 Future Enhancements
 Train and deploy advanced models (e.g., XGBoost, LSTM)

 Push alerts via SMS/Telegram on status change

 Android App for dashboard viewing

 Add SD card logging to hub for offline backup

 Add buzzer/alarm when critical levels detected

