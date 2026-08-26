# mini-DVR
Build a mini dvr for video processing, plus some features
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
