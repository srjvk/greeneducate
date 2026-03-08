from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.quiz_routes import quiz_bp
from routes.pdf_routes import pdf_bp
from routes.learning_routes import learning_bp
from routes.search_routes import search_bp
from routes.sustainability_routes import sustainability_bp
from routes.translation_routes import translation_bp


import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app,resources={r"/api/*": {"origins":"*"}})

    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
    app.config["VECTORSTORE_PATH"] = os.path.join(os.path.dirname(__file__), "vectorstore")
    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY","sat-dev-secret")

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["VECTORSTORE_PATH"], exist_ok=True)

    app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
    app.register_blueprint(pdf_bp, url_prefix="/api/pdf")
    app.register_blueprint(learning_bp, url_prefix="/api/learning")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(sustainability_bp, url_prefix="/api/sustainability")
    app.register_blueprint(translation_bp, url_prefix="/api/translation")

    @app.route("/api/health") 
    def health():
        return {"status":"ok", "service":"Sustainable Agentic Tutor API"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8080)


    





