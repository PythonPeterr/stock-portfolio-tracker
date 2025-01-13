from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/uploads'

    # Import and register blueprints after app initialization
    from .routes import main
    app.register_blueprint(main)

    return app
