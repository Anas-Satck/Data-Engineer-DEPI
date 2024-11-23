# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy         

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__, template_folder='../templates')  # Specify the template folder
#     app.config.from_object('app.config.Config')  # Load configuration from Config class

#     db.init_app(app)  # Initialize the SQLAlchemy instance with the app

#     with app.app_context():
#         from app.models import Product  # Import models here to avoid circular imports
#         db.create_all()  # Create database tables

#     from app.routes import main  # Import routes
#     app.register_blueprint(main)  # Register the blueprint

#     return app


from flask import Flask
from flask_sqlalchemy import SQLAlchemy         

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')  # Specify the template folder
    app.config.from_object('app.config.Config')  # Load configuration from Config class

    db.init_app(app)  # Initialize the SQLAlchemy instance with the app

    with app.app_context():
        from app.models import Product  # Import models here to avoid circular imports
        db.create_all()  # Create database tables

    from app.routes import main  # Import routes
    app.register_blueprint(main)  # Register the blueprint

    return app
