from flask import Flask, request, jsonify,render_template, redirect, url_for,session,message_flashed,send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
def create_app():
    """Construct the core application."""
    
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        from .exam.exam_routes import exams
        from .auth import auth_routes
        app.register_blueprint(exams)
        db.create_all()
        return app