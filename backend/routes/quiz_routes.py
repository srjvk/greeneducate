from flask import Blueprint, request, jsonify
from modules.quiz_analyzer import analyze_quiz
from modules.sustainability import record_request

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    questions = data.get("questions", [])
    subject   = data.get("subject", "general")

    if not questions:
        return jsonify({"error": "No questions provided"}), 400

    try:
        result = analyze_quiz(questions, subject)

        # Rough token estimate for sustainability tracking
        record_request(tokens_used=len(str(questions)) // 4, model="local")
        return jsonify({"status": "ok", "analysis": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500