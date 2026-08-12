# mini-DVR
Build a mini dvr for video processing, plus some features
<img width="960" height="720" alt="image" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFQCWYmOt4VpgAy1Yb8vCi_eZk-Q-d7RZHSBXKuJUHQDOmoQb_rs9rIwCrnCjtSJGuWSsJ1MOgaCaprFTiCauZwVjHT45A1yP1yVkkLo9J5Dlw7Iz8cJpZ14n37MoR5FdQKqJGmlUFhaLvvZV-dc2zQ3_WJaLr74ol4tk_BWK7pQ7u4e2wZJ_4t2D8_vY/s1092/gfgdf8.jpg" />

# 🛰️ AI Smart CCTV

An AI-powered CCTV/DVR platform for **real-time people and vehicle surveillance** using Computer Vision.

## 🚀 Features

- 👤 Person detection & tracking
- 🚗 Vehicle detection & tracking
- 📊 People & vehicle counting
- ↔️ IN/OUT counting with configurable lines
- 🧑 Face detection & recognition
- 🔤 License plate detection & OCR
- 🚨 Intrusion & restricted-zone detection
- 📹 DVR video recording
- 📡 Speed / radar integration
- 📈 Surveillance analytics
- 🌐 Web dashboard

## 🧠 Architecture

```text
Camera / Video
      ↓
 YOLO Detection
      ↓
    Tracking
      ↓
 ┌────┴─────────────┐
 │                  │
Person            Vehicle
 │                  │
 ├─ Face            ├─ Plate
 ├─ Counting        ├─ OCR
 └─ Intrusion       ├─ Counting
                    └─ Speed
 │                  │
 └────────┬─────────┘
          ↓
    Event Engine
          ↓
 Recording + Database
          ↓
      Dashboard
