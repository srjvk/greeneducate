import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from modules.rag import ingest_pdf

pdf_bp = Blueprint("pdf", __name__)
ALLOWED = {"pdf"}

def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

@pdf_bp.route("/upload", methods=["POST"])
def upload():
    
    if "file" not in request.files:
        return jsonify({"error": "No file field in request"}), 400

    file = request.files["file"]
    if file.filename == "" or not _allowed(file.filename):
        return jsonify({"error": "Invalid or missing PDF file"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        info = ingest_pdf(save_path)
        return jsonify({"status": "ingested", **info})
    except Exception as e:
        return jsonify({"error": str(e)}), 500