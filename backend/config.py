# config.py - put in backend/
# Edit the values below for your MySQL setup

DB_CONFIG = {
    "host": "localhost",
    "user": "smart_fridge_user",  
    "password": "123456",
    "database": "smart_fridge",
    "port": 3306
}

# Where uploaded/static files live (relative to this file)
STATIC_VIDEO_DIR = "static/videos"
STATIC_THUMB_DIR = "static/thumbs"
UPLOAD_DIR = "uploads"

# Flask settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
