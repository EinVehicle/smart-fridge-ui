# Smart Fridge Monitoring System — API Specification
*Version: Draft — Week 6*

This document specifies the backend API for the Smart Fridge Monitoring System.  
**Note:** The backend service is not implemented yet. All URLs and responses below are placeholders for future development.

---

## Base URL

Development (local):
http://localhost:5000

Production (TBD):
<to be assigned by hosting provider or UCI server> ```

1. Fridge Overview API
GET /api/fridge/overview

Returns the current status of the fridge sensors and system.

Example Request
GET /api/fridge/overview
Example Response
{
  "sensor": "online",
  "power": "online",
  "door_open": false,
  "empty_slots": 3,
  "last_updated": "2025-11-05T22:30:00Z"
}

Fields
Field	        Type	    Description
sensor	        string	    "online" or "offline" depending on hardware connectivity
power	        string	    "online" or "offline" to indicate power status
door_open	    boolean	    Fridge door status
empty_slots	    integer	    Number of empty spaces in the fridge
last_updated	string	    ISO8601 timestamp of last sensor update

2. Video Metadata API
GET /api/videos

Returns a list of recorded videos and thumbnail data.

Example Response
{
  "videos": [
    {
      "id": 1,
      "filename": "video1.mp4",
      "thumbnail": "thumb1.jpg",
      "timestamp": "2025-11-05T21:00:00Z"
    },
    {
      "id": 2,
      "filename": "video2.mp4",
      "thumbnail": "thumb2.jpg",
      "timestamp": "2025-11-05T21:10:00Z"
    }
  ]
}

3. AI Analysis API
GET /api/analysis

Returns AI-generated analysis results for the latest fridge events.

Example Response
{
  "summary": "Detected 2 items removed and 1 item added.",
  "events": [
    {
      "type": "removed",
      "item": "Milk",
      "time": "2025-11-05T20:10:00Z"
    },
    {
      "type": "added",
      "item": "Orange Juice",
      "time": "2025-11-05T20:11:00Z"
    }
  ]
}

4. Sensor Data Upload API (Hardware → Backend)
POST /api/sensor/update

Hardware sensor nodes will send JSON data to backend.

Example Request Body
{
  "sensor": "online",
  "power": "online",
  "door_open": false,
  "empty_slots": 2
}
Example Response
{
  "status": "ok",
  "received_at": "2025-11-05T22:35:00Z"
}

5. Video Upload API (Camera → Backend)
POST /api/videos/upload

Used by the camera module to upload new video files.

Multipart Form Data
file: <binary video file>
timestamp: <string>
Example Response
{
  "status": "uploaded",
  "video_id": 12
}

6. Error Codes
Code	Meaning
400	    Bad request JSON or missing fields
401	    Unauthorized (if API keys added later)
404	    Resource not found
500	    Internal server error (backend crash or DB error)

7. Notes & Future Work

Integration with real hardware sensors pending completion by teammate.

AI module (video analysis) also pending teammate’s work.

Backend server (Flask/FastAPI/Django) must be set up to support multiple users.

When backend is implemented, this API.md will be updated with real endpoints and authentication.