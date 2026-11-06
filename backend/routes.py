from . import app
import os
import json

from pathlib import Path
from flask import jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import json_util


# --------------------------------------------------
# Load songs.json
# --------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parent
json_url = SITE_ROOT / "data" / "songs.json"

with json_url.open(encoding="utf-8") as file:
    songs_list = json.load(file)


# --------------------------------------------------
# MongoDB configuration
# --------------------------------------------------

mongodb_service = os.getenv("MONGODB_SERVICE", "localhost")
mongodb_port = int(os.getenv("MONGODB_PORT", "27017"))
mongodb_database = os.getenv("MONGODB_DATABASE", "songs")


# --------------------------------------------------
# MongoDB connection
# --------------------------------------------------

client = MongoClient(
    host=mongodb_service,
    port=mongodb_port,
    serverSelectionTimeoutMS=5000
)

client.admin.command("ping")

app.logger.info("MongoDB connected successfully")

db = client[mongodb_database]

songs_collection = db.songs


# --------------------------------------------------
# Initialize database
# --------------------------------------------------

if songs_collection.count_documents({}) == 0:
    if songs_list:
        songs_collection.insert_many(songs_list)


# --------------------------------------------------
# JSON parser
# --------------------------------------------------

def parse_json(data):
    return json.loads(json_util.dumps(data))


# --------------------------------------------------
# 7.1 HEALTH
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def healthz():
    try:
        client.admin.command("ping")
        return jsonify({"status": "OK"}), 200
    except PyMongoError:
        return jsonify({"status": "ERROR"}), 503


# --------------------------------------------------
# 7.2 COUNT
# --------------------------------------------------

@app.route("/count", methods=["GET"])
def count():
    total = songs_collection.count_documents({})
    return jsonify({"count": total}), 200


# --------------------------------------------------
# 7.3 GET ALL SONGS
# --------------------------------------------------

@app.route("/song", methods=["GET"])
def songs():
    results = list(songs_collection.find({}))
    return jsonify({"songs": parse_json(results)}), 200


# --------------------------------------------------
# 7.4 GET SONG BY ID
# --------------------------------------------------

@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = songs_collection.find_one({"id": id})

    if song is None:
        return jsonify({
            "message": f"Song with id {id} not found"
        }), 404

    return jsonify(parse_json(song)), 200


# --------------------------------------------------
# 7.5 POST - CREATE SONG
# --------------------------------------------------

@app.route("/song", methods=["POST"])
def create_song():

    song_in = request.get_json(silent=True)

    if not isinstance(song_in, dict):
        return jsonify({
            "message": "Invalid JSON request"
        }), 400

    if "id" not in song_in:
        return jsonify({
            "message": "Song ID is required"
        }), 400

    existing_song = songs_collection.find_one({
        "id": song_in["id"]
    })

    if existing_song:
        return jsonify({
            "message": "Song already exists"
        }), 409

    result = songs_collection.insert_one(song_in)

    return jsonify({
        "inserted_id": str(result.inserted_id)
    }), 201


# --------------------------------------------------
# 7.6 PUT - UPDATE SONG
# --------------------------------------------------

@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):

    song_in = request.get_json(silent=True)

    if not isinstance(song_in, dict):
        return jsonify({
            "message": "Invalid JSON request"
        }), 400

    if "id" in song_in and song_in["id"] != id:
        return jsonify({
            "message": "Song ID cannot be changed"
        }), 400

    existing_song = songs_collection.find_one({"id": id})

    if existing_song is None:
        return jsonify({
            "message": "Song not found"
        }), 404

    song_in.pop("_id", None)

    songs_collection.update_one(
        {"id": id},
        {"$set": song_in}
    )

    updated_song = songs_collection.find_one({"id": id})

    return jsonify(parse_json(updated_song)), 200


# --------------------------------------------------
# 7.7 DELETE SONG
# --------------------------------------------------

@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):

    result = songs_collection.delete_one({"id": id})

    if result.deleted_count == 0:
        return jsonify({
            "message": "Song not found"
        }), 404

    return "", 204

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "application": "Songs REST API",
        "status": "running",
        "endpoints": [
            "/health",
            "/count",
            "/song",
            "/song/<id>"
        ]
    }), 200
