# Flask App Initialization
from flask import Flask
from flask_login import LoginManager, current_user
from .models import db, init_db, User
import os
from dotenv import load_dotenv

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config.from_object("config.Config")
    
    # Session configuration
    app.secret_key = app.config['SECRET_KEY']

    db.init_app(app)
    login_manager.init_app(app)
    
    # Make current_user available in templates
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    with app.app_context():
        init_db(app)
        # Ensure database schema is up to date
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            if 'book' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('book')]
                if 'isbn' not in columns:
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE book ADD COLUMN isbn VARCHAR(20)"))
                        conn.commit()
        except Exception as e:
            print(f"Schema update note: {e}")

    from .main.routes import main
    from .elearning.routes import elearning
    from .elibrary.routes import elibrary
    from .auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(elearning, url_prefix="/elearning")
    app.register_blueprint(elibrary, url_prefix="/elibrary")
    app.register_blueprint(auth, url_prefix="/auth")

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
