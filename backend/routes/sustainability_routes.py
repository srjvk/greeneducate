from flask import Blueprint, jsonify
from modules.sustainability import get_session_metrics, session_log

sustainability_bp = Blueprint("sustainability", __name__)

@sustainability_bp.route("/metrics", methods=["GET"])
def metrics():
    """GET /api/sustainability/metrics"""
    return jsonify({"status": "ok", "metrics": get_session_metrics()})

@sustainability_bp.route("/reset", methods=["POST"])
def reset():
    """POST /api/sustainability/reset — clear session log."""
    session_log.clear()
    return jsonify({"status": "ok", "message": "Session metrics reset."})