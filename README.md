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

📁 ui/
┣ 📄 index.html → Main web page
┣ 📄 style.css → Page styling
┣ 📄 scripts.js → JavaScript logic (fetching JSON, dynamic display)
┣ 📄 analysis.json → AI analysis data (auto-generated)
┣ 📄 videos.json → Video metadata
┣ 📁 videos/ → Thumbnails and video files
┃ ┗ 📄 .gitkeep
┗ 📄 README.md → This documentation


---

## 🚀 Run Locally

### Prerequisites
- Python 3.x installed

### Start the server:
```bash
cd ui
python -m http.server 8000
```
then open http://localhost:8000/


team member:
Encong Wu | Software Engineering | encongw@uci.edu
Michael Chang | Software Engineering |  tingkc1@uci.edu
Calvin Ngguyen | Computer Engineering | calvin7@uci.edu 
Ali Bahman | Electrical  Engineering | abahman@uci.edu
Yifei Wang｜Computer Engineering ｜yifeiw47@uci.edu 
