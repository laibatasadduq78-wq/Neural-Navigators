from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from datetime import datetime

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Neural Navigators API running"})

learners_db = [
    {"id": "L001", "name": "Ayesha Khan", "course": "Python Bootcamp", "progress": 22, "status": "struggling"},
    {"id": "L002", "name": "Bilal Raza", "course": "Web Dev", "progress": 35, "status": "struggling"},
    {"id": "L003", "name": "Zara Ahmed", "course": "Python", "progress": 98, "status": "excelling"},
    {"id": "L004", "name": "Omar Sheikh", "course": "Web Dev", "progress": 96, "status": "excelling"},
    {"id": "L005", "name": "Sara Malik", "course": "Data Science", "progress": 18, "status": "struggling"},
    {"id": "L006", "name": "Hamza Tariq", "course": "AI Basics", "progress": 41, "status": "average"},
    {"id": "L007", "name": "Nida Fatima", "course": "AI/ML", "progress": 94, "status": "excelling"},
    {"id": "L008", "name": "Ali Hassan", "course": "Data Science", "progress": 91, "status": "excelling"},
]

@app.route('/api/learners', methods=['GET'])
def get_learners():
    status = request.args.get('status')
    if status:
        filtered = [l for l in learners_db if l['status'] == status]
        return jsonify({"learners": filtered, "count": len(filtered)})
    return jsonify({"learners": learners_db, "count": len(learners_db)})

@app.route('/api/learners/<learner_id>/nudge', methods=['POST'])
def nudge_learner(learner_id):
    learner = next((l for l in learners_db if l['id'] == learner_id), None)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404
    return jsonify({"success": True, "message": f"Nudge sent to {learner['name']}"})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "total_learners": 2418,
        "active_this_week": 1847,
        "completion_rate": 94.2,
        "certificates_issued": 312
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in {'xlsx', 'xls', 'csv'}:
        return jsonify({"error": "File type not allowed"}), 400
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return jsonify({"success": True, "filename": filename})

if __name__ == '__main__':
    print("Neural Navigators LMS Running at http://localhost:5000")
    app.run(debug=True, port=5000)