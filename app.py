from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task list
tasks = [
    {"id": 1, "title": "Learn Flask",          "done": False},
    {"id": 2, "title": "Build CI/CD Pipeline", "done": False},
]


# ─────────────────────────────────────────
# GET  /          → Welcome message
# ─────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Task Manager API"}), 200


# ─────────────────────────────────────────
# GET  /tasks     → List all tasks
# ─────────────────────────────────────────
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


# ─────────────────────────────────────────
# POST /tasks     → Create a new task
# Body: { "title": "My Task" }
# ─────────────────────────────────────────
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id":    len(tasks) + 1,
        "title": data["title"],
        "done":  False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201


# ─────────────────────────────────────────
# GET  /tasks/<id>  → Get single task
# ─────────────────────────────────────────
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


# ─────────────────────────────────────────
# PUT  /tasks/<id>  → Update a task
# Body: { "title": "Updated", "done": true }
# ─────────────────────────────────────────
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "title" in data:
        task["title"] = data["title"]
    if "done" in data:
        task["done"] = data["done"]

    return jsonify(task), 200


# ─────────────────────────────────────────
# DELETE /tasks/<id>  → Delete a task
# ─────────────────────────────────────────
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": f"Task {task_id} deleted successfully"}), 200


# ─────────────────────────────────────────
# PATCH /tasks/<id>/done  → Mark as done
# ─────────────────────────────────────────
@app.route("/tasks/<int:task_id>/done", methods=["PATCH"])
def mark_done(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    task["done"] = True
    return jsonify(task), 200


if __name__ == "__main__":
    app.run(debug=True)
