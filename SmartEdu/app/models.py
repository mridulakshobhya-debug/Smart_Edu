# Database Models
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))  # Store full name for greeting
    profile_picture = db.Column(db.String(255), default='profile_1.png')  # Profile picture filename
    learning_goal = db.Column(db.String(255))  # User's learning goal
    heard_from = db.Column(db.String(255))  # Where they heard about SmartEdu
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructor = db.Column(db.String(120))
    duration = db.Column(db.String(50), default="8 weeks")
    level = db.Column(db.String(50), default="Beginner")
    students = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=4.5)
    price = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120))
    description = db.Column(db.Text)
    isbn = db.Column(db.String(20), unique=True)
    category = db.Column(db.String(100))
    pages = db.Column(db.Integer)
    published_date = db.Column(db.DateTime)
    rating = db.Column(db.Float, default=4.5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(100), nullable=False)
    module_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    information = db.Column(db.Text)  # Rich text content
    video_url = db.Column(db.String(500))  # Video URL (YouTube, Vimeo, etc.)
    video_duration = db.Column(db.String(20), default="45 minutes")
    learning_objectives = db.Column(db.Text)  # JSON list of objectives
    resources = db.Column(db.Text)  # JSON list of downloadable resources
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # a, b, c, or d
    explanation = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    quiz_score = db.Column(db.Integer)  # Percentage score
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_db(app):
    with app.app_context():
        db.create_all()
