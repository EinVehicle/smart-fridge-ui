# app.py
import os
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import json

from config import STATIC_VIDEO_DIR, STATIC_THUMB_DIR, UPLOAD_DIR, HOST, PORT, DEBUG
import db

# ----------------------------
# Paths
# ----------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))           # backend 目录
STATIC_VIDEO_PATH = os.path.join(ROOT, STATIC_VIDEO_DIR)
STATIC_THUMB_PATH = os.path.join(ROOT, STATIC_THUMB_DIR)
UPLOAD_PATH = os.path.join(ROOT, UPLOAD_DIR)
UI_PATH = os.path.abspath(os.path.join(ROOT, "..", "ui"))  # 根目录下的 ui

# Ensure directories exist
os.makedirs(STATIC_VIDEO_PATH, exist_ok=True)
os.makedirs(STATIC_THUMB_PATH, exist_ok=True)
os.makedirs(UPLOAD_PATH, exist_ok=True)

app = Flask(__name__, static_folder=None)  # Serve static manually
CORS(app)  # Allow cross-origin for testing

# ----------------------------
# Helpers
# ----------------------------
def video_record_to_front(row):
    return {
        "id": row.get("id"),
        "title": row.get("title"),
        "time": row.get("upload_time").strftime("%b %d, %Y %I:%M %p") if row.get("upload_time") else None,
        "video": f"/static/videos/{row.get('filename')}",
        "thumb": f"/static/thumbs/{row.get('thumbnail')}" if row.get("thumbnail") else None
    }

# ----------------------------
# API Endpoints
# ----------------------------
@app.route("/api/overview", methods=["GET"])
def api_overview():
    row = db.fetchone_dict(
        "SELECT sensor_status AS sensor, power_status AS power, door_open AS door_open, free_space, last_update "
        "FROM fridge_overview ORDER BY id DESC LIMIT 1"
    )
    if not row:
        return jsonify({
            "sensor": "offline",
            "power": "offline",
            "door": False,
            "free_space": 0,
            "last_updated": None
        })
    return jsonify({
        "sensor": row["sensor"],
        "power": row["power"],
        "door": bool(row["door_open"]),
        "free_space": row.get("free_space"),
        "last_updated": row.get("last_update").isoformat() if row.get("last_update") else None
    })

@app.route("/api/analysis", methods=["GET"])
def api_analysis():
    rows = db.fetchall_dict(
        "SELECT id, item_name, quantity, items_detected, timestamp FROM ai_analysis ORDER BY timestamp DESC LIMIT 10"
    )
    out = []
    for r in rows:
        items_detected = r.get("items_detected")
        if isinstance(items_detected, str):
            try:
                items_detected = json.loads(items_detected)
            except Exception:
                items_detected = []
        out.append({
            "id": r["id"],
            "item_name": r.get("item_name"),
            "quantity": r.get("quantity"),
            "items_detected": items_detected,
            "timestamp": r.get("timestamp").isoformat() if r.get("timestamp") else None
        })
    return jsonify({"items": out})

@app.route("/api/videos", methods=["GET"])
def api_videos():
    rows = db.fetchall_dict(
        "SELECT id, title, filename, thumbnail, upload_time FROM videos ORDER BY upload_time DESC"
    )
    return jsonify([video_record_to_front(r) for r in rows])

@app.route("/api/video/<int:video_id>", methods=["GET"])
def api_video_detail(video_id):
    row = db.fetchone_dict(
        "SELECT id, title, filename, thumbnail, upload_time FROM videos WHERE id=%s",
        (video_id,)
    )
    if not row:
        return abort(404, "Video not found")
    return jsonify({
        "video": video_record_to_front(row),
        "analysis": []
    })

@app.route("/api/ai_result", methods=["POST"])
def api_ai_result():
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "detail": str(e)}), 400

    item_name = payload.get("item_name", "")
    quantity = payload.get("quantity", 1)
    items_detected = payload.get("items_detected", [])
    items_json = json.dumps(items_detected)

    ts = payload.get("timestamp")
    if ts:
        try:
            parsed_ts = datetime.fromisoformat(ts)
            ts_param = parsed_ts.strftime("%Y-%m-%d %H:%M:%S")
        except:
            ts_param = None
    else:
        ts_param = None

    query = "INSERT INTO ai_analysis (item_name, quantity, items_detected, timestamp) VALUES (%s, %s, %s, %s)"
    last_id = db.execute(query, (item_name, quantity, items_json, ts_param))
    return jsonify({"status": "ok", "analysis_id": last_id}), 201

@app.route("/api/videos/upload", methods=["POST"])
def api_video_upload():
    if "video" not in request.files:
        return jsonify({"error": "Missing 'video' file"}), 400

    video = request.files["video"]
    thumbnail = request.files.get("thumbnail")
    title = request.form.get("title", "")
    uploaded_by = request.form.get("uploaded_by")
    ts = request.form.get("upload_time")

    vname = secure_filename(video.filename)
    video_path = os.path.join(STATIC_VIDEO_PATH, vname)
    video.save(video_path)

    thumb_name = None
    if thumbnail:
        tname = secure_filename(thumbnail.filename)
        thumb_path = os.path.join(STATIC_THUMB_PATH, tname)
        thumbnail.save(thumb_path)
        thumb_name = tname

    if ts:
        try:
            parsed = datetime.fromisoformat(ts)
            ts_db = parsed.strftime("%Y-%m-%d %H:%M:%S")
        except:
            ts_db = None
    else:
        ts_db = None

    query = "INSERT INTO videos (title, filename, thumbnail, upload_time, uploaded_by) VALUES (%s, %s, %s, %s, %s)"
    vid = db.execute(query, (title, vname, thumb_name, ts_db, uploaded_by))
    return jsonify({
        "status": "uploaded",
        "video_id": vid,
        "video_url": f"/static/videos/{vname}",
        "thumb_url": f"/static/thumbs/{thumb_name}" if thumb_name else None
    }), 201

# ----------------------------
# Hardware upload docking
# ----------------------------

@app.route("/api/hw/upload", methods=["POST"])
def api_hw_upload():
    """
    接收来自 ESP32 的视频或图片。
    支持:
        - file: 视频或图片文件
        - type: "video" / "image"
        - timestamp: 可选
    """
    if "file" not in request.files:
        return jsonify({"error": "Missing file"}), 400

    f = request.files["file"]
    ftype = request.form.get("type", "image")
    ts_raw = request.form.get("timestamp")

    # 生成时间戳文件名
    now = datetime.now()
    ts = ts_raw if ts_raw else now.strftime("%Y%m%d_%H%M%S")

    # 判断文件类型
    ext = os.path.splitext(f.filename)[1].lower()
    if ext == "":
        ext = ".jpg" if ftype == "image" else ".mp4"

    filename = f"{ts}{ext}"

    if ftype == "video":
        save_path = os.path.join(STATIC_VIDEO_PATH, filename)
    else:
        save_path = os.path.join(UPLOAD_PATH, filename)

    f.save(save_path)

    # 返回给前端/AI
    return jsonify({
        "status": "ok",
        "type": ftype,
        "timestamp": ts,
        "filename": filename,
        "url": f"/static/videos/{filename}" if ftype == "video" else f"/upload/{filename}"
    })

# ----------------------------
# Static file serving
# ----------------------------
@app.route("/static/videos/<path:filename>")
def static_videos(filename):
    return send_from_directory(STATIC_VIDEO_PATH, filename)

@app.route("/static/thumbs/<path:filename>")
def static_thumbs(filename):
    return send_from_directory(STATIC_THUMB_PATH, filename)

# ----------------------------
# Serve UI
# ----------------------------
@app.route("/ui/<path:path>")
def serve_ui_static(path):
    return send_from_directory(UI_PATH, path)

@app.route("/ui")
def serve_index():
    return send_from_directory(UI_PATH, "index.html")

# Root endpoint
@app.route("/")
def index():
    return jsonify({"message": "Smart Fridge backend running"})

# ----------------------------
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
