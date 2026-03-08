from flask import Blueprint, request, jsonify
from modules.translator import detect_language, translate, translate_quiz, SUPPORTED_LANGUAGES

translation_bp = Blueprint("translation", __name__)

@translation_bp.route("/languages", methods=["GET"])
def languages():
    """GET /api/translation/languages — list supported languages."""
    return jsonify({"languages": SUPPORTED_LANGUAGES})

@translation_bp.route("/detect", methods=["POST"])
def detect():
    """POST /api/translation/detect  Body: { "text": "..." }"""
    text = request.get_json(force=True).get("text", "")
    return jsonify({"language": detect_language(text)})

@translation_bp.route("/translate", methods=["POST"])
def translate_text():
    """POST /api/translation/translate  Body: { "text": "...", "target": "French" }"""
    data   = request.get_json(force=True)
    text   = data.get("text", "")
    target = data.get("target", "English")
    return jsonify({"translated": translate(text, target)})

@translation_bp.route("/quiz", methods=["POST"])
def translate_quiz_route():
    """POST /api/translation/quiz  Body: { "questions": [...], "target": "Spanish" }"""
    data      = request.get_json(force=True)
    questions = data.get("questions", [])
    target    = data.get("target", "English")
    return jsonify({"translated_quiz": translate_quiz(questions, target)})