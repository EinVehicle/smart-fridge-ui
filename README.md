# Smart Fridge System

This project is part of our **Senior Design** course.  
It is a prototype system that detects the opening of a refrigerator, records a short video, uploads it for AI analysis, and visualizes the results on a web interface.

---

## 🧠 Project Overview

When the fridge door opens:
1. A camera module records a short video.
2. The video is uploaded via Wi-Fi to the server.
3. An AI model analyzes the video to detect items or events.
4. The results are displayed on the dashboard webpage.

---

## 🧩 System Components

| Component | Description |
|------------|-------------|
| **Camera Module** | Detects fridge door opening and records footage |
| **Wi-Fi Module** | Uploads video to server |
| **AI Analyzer** | Runs image/video recognition to detect food items |
| **Web UI** | Displays analysis results and system status dynamically |

---

## 🖥️ Web UI Preview

- **Fridge Overview:** Shows the sensor status, power status, and available space.
- **AI Analysis:** Lists recognized items and timestamps.
- **Video Timeline:** Displays uploaded video thumbnails (click to watch).

---

## 📂 Project Structure

project_root/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── requirements.txt
│   ├── static/
│   │   ├── videos/
│   │   ├── thumbnails/
│   │   └── analysis/
│   ├── upload/
│   └── mysql/
│       ├── create_table.sql
│
└── ui/
    ├── index.html
    ├── style.css
    └── scripts.js

## Database Schema

Located in: backend/mysql/create_table.sql

---

## API Documentation
See the API specification here:  
 **[API.md](./API.md)**

API Endpoints
POST /upload

Uploads a new video.

Request:
Content-Type: multipart/form-data
file: <video.mp4>

Response:
{
  "status": "success",
  "video_id": 12
}

GET /videos

Returns all videos with thumbnail & analysis info.

Response example:
[
  {
    "id": 1,
    "filename": "clip_001.mp4",
    "video_url": "/static/videos/clip_001.mp4",
    "thumbnail_url": "/static/thumbnails/clip_001.jpg",
    "analysis": { "items": ["milk", "eggs"] }
  }
]



## 🚀 Run Server
1. Backend Setup
cd backend
pip install -r requirements.txt //install environment
source venv/bin/activate //active environment
python app.py //start server

Server start at:
http://127.0.0.1:5000

2. Frontend
Open in browser:
http://127.0.0.1:5000/ui



NOTE:
The videos/ folder should contain only production video thumbnails; test videos are excluded from GitHub.
All dynamic content (fridge status, AI analysis, videos) is fetched from JSON endpoints served by Flask.
The backend code (app.py) handles API endpoints and database interactions.

team member:
Encong Wu | Software Engineering | encongw@uci.edu
Michael Chang | Software Engineering |  tingkc1@uci.edu
Calvin Ngguyen | Computer Engineering | calvin7@uci.edu 
Ali Bahman | Electrical  Engineering | abahman@uci.edu
Yifei Wang｜Computer Engineering ｜yifeiw47@uci.edu 
