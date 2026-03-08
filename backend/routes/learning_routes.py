from flask import Blueprint, request, jsonify
from modules.rag import retrieve
from modules.llm_client import generate
from modules.sustainability import record_request
import json

learning_bp = Blueprint("learning", __name__)

LEARNING_PATH_SYSTEM = """
You are an expert curriculum designer and tutor.
Given:
- A student's quiz analysis (strengths, weaknesses, recommended_focus)
- Relevant curriculum excerpts from their textbook

Create a personalized learning path as a JSON object with:
- title: string
- estimated_hours: number
- modules: array of { topic, description, goal, suggested_duration_mins }
Order modules from foundational to advanced, prioritizing weak areas.
Return ONLY valid JSON.
"""

@learning_bp.route("/path", methods=["POST"])
def generate_path():
    data       = request.get_json(force=True)
    analysis   = data.get("analysis", {})
    collection = data.get("collection", "")
    subject    = data.get("subject", "general")

    if not analysis or not collection:
        return jsonify({"error": "Missing analysis or collection"}), 400

    # Retrieve relevant curriculum chunks
    focus = analysis.get("recommended_focus", "general concepts")
    chunks = retrieve(focus, collection_name=collection, k=6)
    context = "\n---\n".join(chunks)

    prompt = (
        f"Student analysis:\n{json.dumps(analysis, indent=2)}\n\n"
        f"Curriculum excerpts:\n{context}"
    )

    try:
        raw = generate(prompt=prompt, subject=subject, system=LEARNING_PATH_SYSTEM)
        clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
        path = json.loads(clean)
        record_request(tokens_used=(len(prompt) + len(raw)) // 4)
        return jsonify({"status": "ok", "learning_path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500