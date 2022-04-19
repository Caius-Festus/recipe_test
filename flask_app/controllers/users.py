from flask import render_template, request, redirect, session
from flask_app import app, Bcrypt, flash
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    session['check'] = 'register'
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "date_of_birth" : request.form["date_of_birth"],
        "password" : request.form["password"],
        "confirm_password" : request.form["confirm_password"]
    }
    if not User.validate_registration(data):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['password'] = pw_hash
    user_id = User.add_user(data)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    session['check'] = 'login'
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not User.validate_login(data):
        return redirect("/")
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db["password"], request.form["password"]):
        flash("Wrong Password")
        return redirect("/")
    session['user_id'] = user_in_db['id']
    session['first_name'] = user_in_db['first_name']
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "user_id" : session["user_id"]
    }
    created_recipes = User.recipes_created_by_user(data)
    return render_template("dashboard.html", created_recipes=created_recipes)