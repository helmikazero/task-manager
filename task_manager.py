from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_USER = os.getenv("MONGO_USER", "mongoadmin")
MONGO_PASS = os.getenv("MONGO_PASS", "password")
MONGO_DB   = os.getenv("MONGO_DB", "task_db")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db["tasks"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = list(collection.find({}, {"_id": 0}))
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    required = {"title", "create_day", "due_days"}
    if not required.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400
    collection.insert_one(data)
    return jsonify({"message": "Task added successfully"})

@app.route("/api/tasks/<title>", methods=["DELETE"])
def delete_task(title):
    result = collection.delete_one({"title": title})
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
