# 🔧 ESP32-Based Machine Health Monitoring System

This project implements a **Machine Health Monitoring System** using multiple **ESP32 boards**. It gathers **temperature**, **humidity**, and **sound level** data from sensor nodes and sends it wirelessly to a central hub using **ESP-NOW**. The hub visualizes real-time sensor data on a web dashboard and uploads it to **Google Sheets** for remote logging and **machine health status** evaluation.

---

## 📦 Features

- 📡 **ESP-NOW Communication** between sensor nodes and hub  
- 🌐 **Web Dashboard** with live charts using Chart.js  
- 📈 **Google Sheets Integration** via Google Apps Script  
- 🧠 **Health Status Evaluation** based on sensor thresholds  
- 🖥️ **Real-time HTML Interface** hosted on the hub  
- ☁️ **Cloud Logging** with timestamped entries  
- 🛠️ Lightweight and scalable design  

---

## 🔧 Hardware Used

- 🔌 **ESP32 Development Boards** (at least 2: one hub, one or more nodes)  
- 🌡️ **DHT11 Sensor** for temperature and humidity  
- 🎤 **Analog Sound Sensor** (connected to an analog input pin)  
- 📶 **Wi-Fi Access Point** for hosting dashboard and uploading to cloud  

---

## 🗂️ Project Structure
machine-health-monitor/
├── /hub/
│   └── hub_code.ino            → Receives ESP-NOW data, serves dashboard, uploads to Google Sheets
├── /node/
│   └── node_code.ino           → Sends DHT + sound data to the hub using ESP-NOW
├── /mac_reader/
│   └── get_mac_address.ino     → Use this to retrieve ESP32 MAC addresses
├── /google_script/
│   └── code.gs                 → Google Apps Script to log data in Google Sheets
└── README.md



---

## ⚙️ How It Works

### 1. Sensor Node (ESP32)

- Reads **temperature** and **humidity** using the **DHT11 sensor**  
- Reads **sound level** via analog input pin  
- Sends sensor data to the **hub ESP32** using **ESP-NOW** protocol  

### 2. Hub ESP32

- Receives data from multiple sensor nodes via **ESP-NOW**  
- Hosts a **web server (port 80)** that shows:
  - Live sensor values
  - Time-stamped data
  - Color-coded health status
- Sends data to a **Google Sheet** using a GET request to a deployed **Google Apps Script Web App**

### 3. Google Sheet

- Logs each data point with:
  - Timestamp
  - Temperature
  - Humidity
  - Sound Level
  - Machine Health Status (e.g., Normal, Warning, Critical)
- Can be used for historical analysis, graphing, or integration with ML models

---

## 🌐 Web Dashboard (Hosted on Hub)

The hub serves a user-friendly HTML page with:
- Live sensor data in real time  
- Visual indicators (green/yellow/red) for machine health  
- Refreshing data every few seconds  
- Responsive design for mobile/desktop viewing  

---

## 📈 Google Sheets Logging

### Deployment Steps:
1. Open `code.gs` in your Google Script Editor
2. Deploy it as a **Web App** with **"Anyone with the link"** access
3. Copy the generated Web App URL
4. Add this URL in `hub_code.ino` for Google Sheets logging

---

## 🧪 Health Status Logic

Status is determined by comparing sensor readings against thresholds:

| Sensor       | Threshold Example      | Status Condition            |
|--------------|------------------------|-----------------------------|
| Temperature  | > 45°C                 | ⚠️ Warning / 🔴 Critical     |
| Humidity     | > 80% or < 30%         | ⚠️ Warning                  |
| Sound Level  | > 60 dB (analog level) | ⚠️ Warning / 🔴 Critical     |

Status is color-coded and displayed on the dashboard.

---

## 📋 Example Data Entry in Google Sheet

| Timestamp           | Temperature | Humidity | Sound | Status         |
|---------------------|-------------|----------|--------|----------------|
| 2025-07-12 15:23:01 | 43.5 °C     | 78.0 %   | 55.2   | Normal         |
| 2025-07-12 15:28:15 | 47.2 °C     | 84.3 %   | 62.5   | Needs Maintenance |

---

## 🚀 Setup Instructions

1. **Get MAC addresses** of all ESP32s using `mac_reader/get_mac_address.ino`
2. Update MAC addresses in `node_code.ino` and `hub_code.ino`
3. Deploy Google Apps Script (`code.gs`) and get the Web App URL
4. Flash `node_code.ino` to sender ESP32s
5. Flash `hub_code.ino` to receiver ESP32 (hub)
6. Connect hub ESP32 to Wi-Fi and open the IP in a browser to view the dashboard

---

## ✅ To Do / Future Enhancements

- 🧠 Integrate with ML-based health prediction models  
- 📊 Plot historical data using Google Charts or Chart.js  
- 📱 Create a mobile app to view machine status  
- 🔔 Add real-time alert notifications (SMS/email)  
- 💾 Store local backup logs on SD card  

---

## 👩‍💻 Author

**Shibam Mandal**  



If you found this project useful or inspiring:

🌟 Star this repository  
🍴 Fork it  
🐛 Report issues  
💬 Share your suggestions

---


