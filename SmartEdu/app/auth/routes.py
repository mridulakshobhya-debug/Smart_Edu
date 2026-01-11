from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import User, db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username") or request.form.get("email")
        password = request.form.get("password")
        
        # Validate input
        if not username or not password:
            flash("Please enter both username/email and password", "danger")
            return render_template("login.html")
        
        u = User.query.filter_by(username=username).first() or User.query.filter_by(email=username).first()
        
        if u and u.check_password(password):
            login_user(u)
            flash(f"Welcome back, {u.full_name or u.username}!", "success")
            return redirect("/")
        else:
            flash("Invalid username/email or password. Please try again.", "danger")
    return render_template("login.html")

@auth.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        full_name = request.form.get("full_name", "")
        profile_picture = request.form.get("profile_picture", "profile_1.png")
        learning_goal = request.form.get("learning_goal", "")
        heard_from = request.form.get("heard_from", "")
        
        # Validate input
        if not username or not email or not password:
            flash("Please fill in all required fields", "danger")
            return render_template("signup.html")
        
        if len(password) < 6:
            flash("Password must be at least 6 characters long", "danger")
            return render_template("signup.html")
        
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template("signup.html")
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "danger")
            return render_template("signup.html")
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please login instead.", "danger")
            return render_template("signup.html")
        
        # Create new user
        u = User(
            username=username,
            email=email,
            full_name=full_name or username,
            profile_picture=profile_picture,
            learning_goal=learning_goal,
            heard_from=heard_from
        )
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        flash(f"Welcome, {u.full_name}! Your account has been created.", "success")
        return redirect("/")
    return render_template("signup.html")

@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    from flask_login import current_user
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "update_info":
            full_name = request.form.get("full_name")
            learning_goal = request.form.get("learning_goal")
            heard_from = request.form.get("heard_from")
            profile_picture = request.form.get("profile_picture")
            
            if full_name:
                current_user.full_name = full_name
            if learning_goal:
                current_user.learning_goal = learning_goal
            if heard_from:
                current_user.heard_from = heard_from
            if profile_picture:
                current_user.profile_picture = profile_picture
            
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for("auth.profile"))
        
        elif action == "change_password":
            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")
            
            if not current_user.check_password(old_password):
                flash("Current password is incorrect", "danger")
                return redirect(url_for("auth.profile"))
            
            if len(new_password) < 6:
                flash("New password must be at least 6 characters", "danger")
                return redirect(url_for("auth.profile"))
            
            if new_password != confirm_password:
                flash("New passwords do not match", "danger")
                return redirect(url_for("auth.profile"))
            
            current_user.set_password(new_password)
            db.session.commit()
            flash("Password changed successfully!", "success")
            return redirect(url_for("auth.profile"))
        
        elif action == "change_username":
            new_username = request.form.get("new_username")
            
            if not new_username:
                flash("Username cannot be empty", "danger")
                return redirect(url_for("auth.profile"))
            
            if User.query.filter_by(username=new_username).first():
                flash("Username already taken", "danger")
                return redirect(url_for("auth.profile"))
            
            current_user.username = new_username
            db.session.commit()
            flash("Username changed successfully!", "success")
            return redirect(url_for("auth.profile"))
    
    return render_template("profile.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
