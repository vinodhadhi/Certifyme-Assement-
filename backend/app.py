from flask import Flask
from flask_cors import CORS
from extensions import db, migrate
from config import Config
from routes.auth_routes import auth_bp
from routes.opportunity_routes import opportunity_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(opportunity_bp, url_prefix="/api/opportunities")

    # Create tables
    with app.app_context():
        db.create_all()

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return {"status": "ok", "message": "Admin Portal API is running"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
