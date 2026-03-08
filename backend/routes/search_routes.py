from flask import Blueprint, request, jsonify
from modules.search_client import fetch_resources

search_bp = Blueprint("search", __name__)

@search_bp.route("/resources", methods=["POST"])
def resources():
    data   = request.get_json(force=True)
    topics = data.get("topics", [])

    if not topics:
        return jsonify({"error": "No topics provided"}), 400

    results = {}
    for topic in topics[:5]:  # cap at 5 topics per request
        try:
            results[topic] = fetch_resources(topic)
        except Exception as e:
            results[topic] = {"error": str(e)}

    return jsonify({"status": "ok", "resources": results})